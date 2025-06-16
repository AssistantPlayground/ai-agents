from fastapi import APIRouter, HTTPException
from typing import List
from app.api.schemas import Query, Response
from app.services.rag_service import rag_service
from app.dependencies import get_rag_service

router = APIRouter()


@router.post("/initialize", response_model=dict)
async def initialize_knowledge_base(documents: List[str]):
    try:
        rag_service.initialize_knowledge_base(documents)
        return {"status": "success", "message": "Knowledge base initialized"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=Response)
async def query_agent(query: Query):
    try:
        result = rag_service.process_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
