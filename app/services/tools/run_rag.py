from langchain_core.tools import tool
from app.db.weaviate_client import weaviate_client
from fastapi.encoders import jsonable_encoder
from typing import Any


@tool
async def run_rag(user_id: str, message: str) -> list[dict[str, Any]]:
    context = await weaviate_client.search_similar(message, user_id)
    return jsonable_encoder(context)
