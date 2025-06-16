from typing import Optional
import weaviate
from weaviate.classes.query import Filter

from app.schemas.weaviate import DocumentSchema


class WeaviateClient:
    def __init__(self):
        self.client = weaviate.use_async_with_local()


    async def ensure_schema(self):
        async with self.client:
            if not await self.client.collections.exists("Document"):
                await self.client.collections.create(
                    **DocumentSchema.schema()
                )


    async def add_documents(
        self, 
        texts: list[str], 
        user_id: Optional[str] = None, 
        metadata: Optional[dict] = None
    ):
        """Add documents to Weaviate."""
        async with self.client:
            await self.client.is_ready()
            documents = self.client.collections.get("Document")
            documents_data = [{
                "content": text,
                "userId": user_id,
                "metadata": str(metadata) if metadata else None
            } for text in texts]
            response = await documents.data.insert_many(documents_data)
        return response


    async def search_similar(
        self, 
        query: str, 
        user_id: Optional[str] = None, 
        limit: int = 3
    ):
        """Search for similar documents."""
        where_filter = None
        if user_id:
            where_filter = Filter.any_of([
                Filter.by_property("userId").is_none(True),
                Filter.by_property("userId").equal(user_id)
            ])
        async with self.client:
            await self.client.is_ready()
            documents = self.client.collections.get("Document")
            result = await documents.query.near_text(
                query=query,
                limit=limit,
                filters=where_filter
            )
        return result.objects

    async def delete_doc(self, id):
        async with self.client:
            await self.client.is_ready()
            collection = self.client.collections.get("Document")
            await collection.data.delete_by_id(id)


weaviate_client = WeaviateClient()
