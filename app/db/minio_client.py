from fastapi import HTTPException
from minio import Minio

from app.core.config import settings


_client: Minio = Minio(
    f"{settings.MINIO_HOST}:{settings.MINIO_PORT}",
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False
)


def get_minio_client() -> Minio:
    return _client


async def ensure_bucket_exists(client: Minio, bucket_name: str) -> None:
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при проверке/создании bucket: {str(e)}")
