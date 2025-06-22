from fastapi import APIRouter, HTTPException

from app.db.weaviate_client import weaviate_client
from app.core.config import settings
from app.api.rag import schemas

from langchain.document_loaders import S3DirectoryLoader, S3FileLoader


router = APIRouter()


@router.post("")
async def rag(body: schemas.RAGRequest):
    try:
        await weaviate_client.client.connect()
        response = await weaviate_client.search_similar(
            query = body.query, 
            user_id = body.user_id, 
            limit = body.limit
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/load/moc")
async def load_moc_data():
    directory_loader = S3DirectoryLoader(
        bucket='moc',
        prefix='',
        endpoint_url=f"http://{settings.MINIO_HOST}:{settings.MINIO_PORT}",
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        use_ssl=False
    )
    async for document in directory_loader.alazy_load():
        await weaviate_client.add_documents(
            texts = [document.page_content],
            user_id = None,
            metadata = document.metadata
        )


@router.post("/process")
async def process_doc(body: schemas.ProcessDataRequest):
    loader = S3FileLoader(
        bucket = body.bucket,
        key = body.key,
        endpoint_url=f"http://{settings.MINIO_HOST}:{settings.MINIO_PORT}",
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        use_ssl=False
    )
    async for document in loader.alazy_load():
        await weaviate_client.add_documents(
            texts = [document.page_content],
            user_id = body.user_id,
            metadata = document.metadata
        )


@router.delete("/{id}")
async def delete_docs(id: str):
    await weaviate_client.delete_doc(id)
    return {"status": "ok"}