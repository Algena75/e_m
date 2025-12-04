from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String

from app.core.db import Base


class SomeModel(Base):
    """Дополнительная модель."""
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Расширяем модель пользователя из библиотеки FastAPI Users.
    """
    firstname = Column(String(254), nullable=False)
    surname = Column(String(254), nullable=True)
    patronymic = Column(String(254), nullable=True)

    def dict(self):
        return dict(
            id=self.id,
            email=self.email,
            is_superuser=self.is_superuser,
            firstname=self.firstname
        )
