from pydantic import BaseModel
from typing import Dict, Any


class DocumentMetadata(BaseModel):
    content_type: str
    size: int
    additional_info: Dict[str, Any] = {} 


class DocumentResponse(BaseModel):
    metadata: DocumentMetadata
    filename: str
    document_url: str
    status: str = "success"
