import asyncio
import logging

import aiohttp
import aio_pika

from langchain.document_loaders import S3FileLoader

from app.api.media.schemas import DocumentMetadata
from app.core.config import settings
from app.db.weaviate_client import weaviate_client
from app.services.rabbitmq_connection import RabbitQueue


logging.basicConfig(level=logging.INFO)


async def fetch_file(document_url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(document_url) as response:
            if response.status != 200:
                raise ValueError(f"Failed to download file: {response.status}")
            return await response.read()


async def process_document_file(filename: str, file_bytes: bytes, metadata: DocumentMetadata):
    loader = S3FileLoader(
        bucket = metadata.bucket,
        key = metadata.prefix,
        endpoint_url=f"http://{settings.MINIO_HOST}:{settings.MINIO_PORT}",
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        use_ssl=False
    )
    async for document in loader.alazy_load():
        await weaviate_client.add_documents(
            texts = [document.page_content],
            user_id = metadata.user_id,
            metadata = document.metadata
        )

    logging.info(f"Processing of file {filename} completed.")


async def handle_message(body: dict):
    filename = body["filename"]
    document_url = body["document_url"]
    metadata = DocumentMetadata(**body["metadata"])

    logging.info(f"Received message for file: {filename}")

    file_bytes = await fetch_file(document_url)
    await process_document_file(filename, file_bytes, metadata)


async def main():
    logging.info("Starting media file processor...")
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(RabbitQueue.rag.name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        import json
                        body = json.loads(message.body)
                        await handle_message(body)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")
                        continue


if __name__ == "__main__":
    asyncio.run(main())
