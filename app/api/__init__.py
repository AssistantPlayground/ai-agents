from fastapi import APIRouter

from app.api.user import router as user_router
from app.api.media import router as media_router
from app.api.rag import router as rag_router
from app.api.agent import router as agent_router


router = APIRouter()

router.include_router(user_router.router, prefix="/users", tags=["Users"])
router.include_router(media_router.router, prefix="/media", tags=["Media"])
router.include_router(rag_router.router, prefix="/rag", tags=["RAG"])
router.include_router(agent_router.router, prefix="/agent", tags=["Agents"])
