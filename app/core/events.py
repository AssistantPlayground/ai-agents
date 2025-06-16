from app.db.weaviate_client import weaviate_client
from app.services.rabbitmq_connection import rabbit_connection, RabbitQueue
from fastapi import FastAPI


async def setup_event(app: FastAPI):
    # Setup the Weaviate schemas
    await weaviate_client.ensure_schema()
    await rabbit_connection.connect()
    for i in RabbitQueue:
        await rabbit_connection.declare_queue(
            queue_name=i.name.lower(), 
            routing_key=i.value,
            durable=True
        )


async def shutdown_app(app: FastAPI):
    await rabbit_connection.close()
