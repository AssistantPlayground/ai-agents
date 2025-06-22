from langchain_core.tools import tool
from app.db.weaviate_client import weaviate_client


@tool
async def get_medical_tests(message: str):
    context = await weaviate_client.search_similar(message)
    return context
