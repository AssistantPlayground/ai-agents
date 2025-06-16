from odmantic import Model
from app.schemas.mongodb.base import DefaultTags
from typing import Literal


class Document(Model):
    __collection__ = "documents"
    
    url: str
    title: str
    size: int
    type: Literal["application/pdf"]
    tags: list[DefaultTags | str]
    user_id: str
