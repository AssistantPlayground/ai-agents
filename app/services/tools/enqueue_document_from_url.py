import aiohttp
import tempfile
import os
from langchain_core.tools import tool
from app.services.rabbitmq_connection import rabbit_connection, RabbitQueue
from app.schemas.agent import ALLOWED_MIME_TYPES, MAX_FILE_SIZE_MB


@tool
async def enqueue_document_from_url(url: str, user_id: str) -> str:
    await rabbit_connection.connect()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return f"Failed to download file: HTTP {resp.status}"

            content_type = resp.headers.get("Content-Type", "")
            content_length = resp.headers.get("Content-Length")

            if content_type not in ALLOWED_MIME_TYPES:
                return f"Unsupported file type: {content_type}"

            if content_length and int(content_length) > MAX_FILE_SIZE_MB * 1024 * 1024:
                return f"File too large: {int(content_length) / 1024 / 1024:.2f} MB"

            content = await resp.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(url)[-1]) as f:
        f.write(content)
        temp_path = f.name

    metadata = {
        "user_id": user_id,
        "original_url": url,
        "local_path": temp_path,
        "mime_type": content_type
    }

    await rabbit_connection.send_messages(metadata, routing_key=RabbitQueue.rag.value)

    return f"Document from {url} has been queued for processing."
