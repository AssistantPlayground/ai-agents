from odmantic import AIOEngine
from motor import motor_asyncio

from app.core.config import settings


mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
engine = AIOEngine(client=mongo_client, database=settings.MONGO_DATABASE)


def get_engine() -> AIOEngine:
    return engine


__all__ = ["get_engine"]
