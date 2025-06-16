from fastapi import HTTPException, Header
from app.core.config import settings
from typing import Optional


def get_user_id(
    user_id: Optional[str] = Header(None, alias = "X-User-Id")
) -> str:
    if not user_id and settings.ENV == "dev":
        return settings.TEST_USER_ID
    raise HTTPException(status_code=401, detail="Unauthorized")
