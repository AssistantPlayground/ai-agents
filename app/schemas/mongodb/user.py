import enum

from pydantic import BaseModel, ConfigDict
from odmantic import ObjectId


class DefaultTags(enum.Enum):
    PERSONAL = "personal"
    GENERAL = "general"


class UserBase(BaseModel):
    matrix_id: str
    full_name: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: ObjectId | None = None
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    model_config = ConfigDict(populate_by_name=True)

class MatrixUser(BaseModel):
    matrix_id: str
    full_name: str