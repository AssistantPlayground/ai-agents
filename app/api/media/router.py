import uuid
from io import BytesIO
from typing import Literal, BinaryIO

from fastapi import APIRouter, UploadFile, HTTPException, Depends
from minio import Minio

from app.db.minio_client import get_minio_client, ensure_bucket_exists
from app.core.config import settings
from app.api.media.schemas import DocumentResponse, DocumentMetadata
from app.crud.crud_users import user as user_crud
from app.crud.crud_docs import docs as docs_crud
from app.schemas.mongodb.docs import DocumentCreate
from starlette.datastructures import Headers
from app.dependencies import get_user_id
from app.services.rabbitmq_connection import rabbit_connection, RabbitQueue


ALLOWED_FILETYPES = ["pdf", "txt", "doc", "docx"]
ALLOWED_CONTENT_TYPES = ["application/pdf"]

router = APIRouter()


class CustomUploadFile(UploadFile):
    extension: str
    filename: str
    content_type: Literal["application/pdf"]


    def __init__(self,
        file: BinaryIO,
        filename: str,
        size: int | None = None,
        headers: Headers | None = None,
    ):
        super().__init__(file, size=size, filename=filename, headers=headers)
        file_extension = next(
            (
                i for i in ALLOWED_FILETYPES \
                    if filename.lower().endswith(f".{i}") \
                        and self.content_type in ALLOWED_CONTENT_TYPES
            ), None
        )
        if not file_extension:
            raise HTTPException(status_code=400, detail="File type not allowed")
        self.extension = file_extension
        self.filename = f"{uuid.uuid4()}.{file_extension}"


async def get_custom_upload_file(file: UploadFile) -> CustomUploadFile:
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required")
    if not file.content_type:
        raise HTTPException(status_code=400, detail="File type is required")
    return CustomUploadFile(
        filename=file.filename,
        file=file.file,
        headers=file.headers
    )


@router.post("/upload")
async def upload_media(
    matrix_id: str,
    file: CustomUploadFile = Depends(get_custom_upload_file),
    minio_client: Minio = Depends(get_minio_client),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required")
    if not file.content_type:
        raise HTTPException(status_code=400, detail="File type is required")
    
    user = await user_crud.get_by_matrix_id(matrix_id=matrix_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    MINIO_BUCKET = "documents"
    await ensure_bucket_exists(minio_client, MINIO_BUCKET)
    
    try:
        file_data = await file.read()
        file_size = len(file_data)
        file_stream = BytesIO(file_data)
        
        minio_client.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=file.filename,
            data=file_stream,
            length=file_size,
            content_type=file.content_type
        )
        # http://localhost:9001/api/v1/buckets/documents/objects/download?prefix=8d2f2374-16bb-487d-aede-47bc42ed5ed6.pdf
        document_url = f"{settings.MINIO_HOST}:{settings.MINIO_PORT}/api/v1/buckets/{MINIO_BUCKET}/objects/download?prefix={file.filename}"
        metadata = DocumentMetadata(
            content_type=file.content_type,
            size=file_size,
            additional_info={"original_filename": file.filename},
            buckets=MINIO_BUCKET,
            prefix=file.filename,
            user_id=str(user.id)
        )

        await docs_crud.create(obj_in=DocumentCreate(
            url=document_url,
            title=file.filename,
            size=file_size,
            type=file.content_type,
            tags=[],
            user_id=str(user.id)
        ))
        
        await rabbit_connection.send_messages(
            messages={
                "filename": file.filename,
                "document_url": document_url,
                "metadata": metadata.model_dump(),
            },
            routing_key=RabbitQueue.rag.value
        )

        return DocumentResponse(
            filename=file.filename,
            document_url=document_url,
            metadata=metadata,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {str(e)}") 


@router.get("")
async def get_media_list(
    page: int | None = None,
    limit: int | None = None
):
    await docs_crud.get_multi(
        page=page,
        limit=limit,
        page_break=True
    )


@router.get("/{media_id}")
async def get_media(
    user_id: str = Depends(get_user_id)
):
    doc = await docs_crud.get(user_id)
    if not doc:
        raise HTTPException(
            404,
            "Media file is not found"
        )
    
