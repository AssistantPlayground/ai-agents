from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    content: str


class DocumentInput(BaseModel):
    content: str
    metadata: Optional[dict] = None


class Response(BaseModel):
    response: str
