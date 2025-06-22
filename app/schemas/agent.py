from typing import Dict, Any, TypedDict


class User(TypedDict):
    user_id: str


class AgentState(TypedDict):
    user: User
    message: str
    context: list[Dict[str, Any]] | None
    response: str


ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

MAX_FILE_SIZE_MB = 10
