from pydantic import BaseModel
from typing import List

class Query(BaseModel):
    question: str
    context: str = ""

class Response(BaseModel):
    answer: str
    sources: List[str] = [] 