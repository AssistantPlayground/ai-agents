from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from pydantic import BaseModel

from app.services.agent_service import agent_service
from app.api.agent.schemas import Message
from app.dependencies import get_user_id


router = APIRouter(prefix="/agent")


class AgentState(BaseModel):
    message: str
    context: list[Dict[str, Any]] | None
    response: str

@router.post("/chat", response_model=AgentState)
async def chat(message: Message, user_id: str = Depends(get_user_id)) -> AgentState:
    try:
        response = await agent_service.process_message(message.content, user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
