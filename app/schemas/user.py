from fastapi_users import schemas
from typing import Optional

from pydantic import BaseModel, Field


class UserFIO(BaseModel):
    firstname: str = Field(..., min_length=2, max_length=254)
    surname: Optional[str] = Field(None, min_length=2, max_length=254)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=254)



class UserRead(schemas.BaseUser[int], UserFIO):
    pass


class UserCreate(schemas.BaseUserCreate, UserFIO):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserFIO):
    firstname: Optional[str] = Field(None, min_length=2, max_length=254)
