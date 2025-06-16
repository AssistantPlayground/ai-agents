from pydantic import BaseModel
from typing import Dict, Any


class RAGRequest(BaseModel):
    query: str
    user_id: str | None = None
    limit: int = 3


class ProcessDataRequest(BaseModel):
    url: str
    user_id: str
    bucket: str
    key: str
