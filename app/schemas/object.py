from pydantic import BaseModel


class ObjectCreate(BaseModel):
    pass


class ObjectRead(ObjectCreate):
    pass


class ObjectUpdate(ObjectCreate):
    pass
