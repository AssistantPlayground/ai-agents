from fastapi import APIRouter

from app.models.user import User
from app.crud.crud_users import user as user_crud
from app.schemas.mongodb.user import UserCreate


router = APIRouter()


@router.post("/ensure_registered")
async def ensure_registered(user: UserCreate) -> User:
    db_user = await user_crud.get_by_matrix_id(matrix_id=user.matrix_id)
    if not db_user:
        db_user = await user_crud.create(obj_in=user)
    return db_user
