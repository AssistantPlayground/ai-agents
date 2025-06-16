import weaviate.classes as wvc
from pydantic import BaseModel
from app.core.config import settings
from weaviate.collections.classes.config_vectorizers import _VectorizerConfigCreate, _Text2VecOllamaConfig


class WeaviateSchema(BaseModel):
    name: str
    vectorizer_config: _VectorizerConfigCreate
    properties: list[wvc.config.Property]
    

class DocumentSchema(WeaviateSchema):
    name: str = "Document"
    vectorizer_config: _VectorizerConfigCreate = wvc.config.Configure.Vectorizer.text2vec_ollama(
        api_endpoint=settings.WEAVIATE_OLLAMA,
        model=settings.EMBEDDING_MODEL
    )
    # inverted_index_config=wvc.config.Configure.inverted_index(
    #     bm25_b=0.7,
    #     bm25_k1=1.25,
    #     index_null_state=True,
    #     index_property_length=True,
    #     index_timestamps=True
    # )
    inverted_index_config: BaseModel = wvc.config.Configure.inverted_index(
        bm25_b=0.7,
        bm25_k1=1.25,
        index_null_state=True,
        index_property_length=True,
        index_timestamps=True
    )
    properties: list[wvc.config.Property] = [
        wvc.config.Property(
            name="content",
            data_type=wvc.config.DataType.TEXT,
            description="The content of the document"
        ),
        wvc.config.Property(
            name="userId",
            data_type=wvc.config.DataType.TEXT,
            index_filterable=True,
            description="The ID of the user who owns this document"
        ),
        wvc.config.Property(
            name="metadata",
            data_type=wvc.config.DataType.TEXT,
            description="Additional metadata about the document"
        )
    ]

    @classmethod
    def schema(cls: type['DocumentSchema']) -> dict:
        instance = cls()
        return {
            "name": instance.name,
            "vectorizer_config": instance.vectorizer_config,
            "properties": instance.properties,
            "inverted_index_config": instance.inverted_index_config
        }
    