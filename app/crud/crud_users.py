from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.mongodb.user import UserCreate, UserUpdate, MatrixUser
from app.exceptions import IsNotImplemented


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_matrix_id(self, *, matrix_id: str) -> User | None: # noqa
        return await self.engine.find_one(User, User.matrix_id == matrix_id)


    async def update(self, *args, **kwargs) -> User: # noqa
        raise IsNotImplemented("CRUDUser.update not implemented")


    async def remove(self, *args, **kwargs) -> User: # noqa
        raise IsNotImplemented("CRUDUser.update not implemented")


user = CRUDUser(User)
