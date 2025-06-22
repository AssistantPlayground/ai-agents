import json
from dataclasses import dataclass
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue, AbstractExchange
from app.core.config import settings
import enum


class RabbitQueue(enum.Enum):
    rag = 'tasks.rag.process_document'

@dataclass
class RabbitConnection:
    _connection: AbstractRobustConnection | None = None
    _channel: AbstractChannel | None = None
    _exchange: AbstractExchange | None = None


    async def connect(self):
        if self.status():
            return

        self._connection = await connect_robust(settings.CELERY_BROKER_URL)
        self._channel = await self._connection.channel(publisher_confirms=False)

        self._exchange = await self._channel.declare_exchange(
            name="rag",
            type=ExchangeType.DIRECT,
            durable=True
        )


    def status(self) -> bool:
        return bool(
            (self._connection and not self._connection.is_closed)
            and (self._channel and not self._channel.is_closed)
        )


    async def declare_queue(self, queue_name: str, *, routing_key: str | None = None, **kwargs) -> AbstractQueue:
        if not self.status():
            raise RuntimeError("RabbitMQ is not connected.")

        queue = await self._channel.declare_queue(queue_name, **kwargs)  # type: ignore
        if routing_key:
            await queue.bind(self._exchange, routing_key=routing_key)  # type: ignore
        return queue


    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()


    async def send_messages(self, messages: list | dict, routing_key: str) -> None:
        """
            Public message or messages to the RabbitMQ queue.

            :param messages: list or dict with messages objects.
            :param routing_key: Routing key of RabbitMQ, not required. Tip: the same as in the consumer.
        """
        if not self._channel:
            raise RuntimeError('The message could not be sent because the connection with RabbitMQ is not established')

        if isinstance(messages, dict):
            messages = [messages]

        async with self._channel.transaction():
            for message in messages:
                message = Message(
                    body=json.dumps(message).encode()
                )

                await self._exchange.publish(message, routing_key)  # type: ignore


rabbit_connection = RabbitConnection()
