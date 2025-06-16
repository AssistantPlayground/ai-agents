import asyncio

import aio_pika

from app.services.rabbitmq_connection import RabbitQueue


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(RabbitQueue.rag.name, durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break


if __name__ == "__main__":
    asyncio.run(main())




import asyncio
import logging
from .document_service import DocumentService
from .config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main application entry point"""
    settings = get_settings()
    
    # Initialize document service
    service = DocumentService(
        rabbitmq_url=settings.RABBITMQ_URL,
        mongodb_url=settings.MONGODB_URL,
        minio_endpoint=settings.MINIO_ENDPOINT,
        minio_access_key=settings.MINIO_ACCESS_KEY,
        minio_secret_key=settings.MINIO_SECRET_KEY,
        minio_bucket=settings.MINIO_BUCKET
    )
    
    try:
        # Connect to RabbitMQ and start processing
        await service.connect()
        logger.info("Document processing service started")
        
        # Keep the service running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down document processing service")
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
    finally:
        await service.close()

if __name__ == "__main__":
    asyncio.run(main()) 