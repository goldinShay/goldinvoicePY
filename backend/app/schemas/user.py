from pydantic import BaseModel
from typing import Optional
from app.models.enums import Role

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Optional[Role] = Role.USER

class UserRead(UserBase):
    id: int
    role: Role

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str
