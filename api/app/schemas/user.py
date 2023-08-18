from typing import Optional
from pydantic import UUID4, BaseModel


class UserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: str


class ShowUser(UserBase):
    id: UUID4


