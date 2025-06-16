from typing import Literal

from pydantic import BaseModel, ConfigDict
from odmantic import ObjectId


from app.schemas.mongodb.base import DefaultTags


class DocumentBase(BaseModel):
    url: str
    title: str
    size: int
    type: Literal["application/pdf"]
    tags: list[DefaultTags | str]
    user_id: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDBBase(DocumentBase):
    id: ObjectId | None = None
    model_config = ConfigDict(from_attributes=True)


class Document(DocumentInDBBase):
    model_config = ConfigDict(populate_by_name=True)
