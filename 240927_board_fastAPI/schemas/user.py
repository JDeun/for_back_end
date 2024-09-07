from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    receive_ads: int

class UserCreate(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: str

    class Config:
        orm_mode = True
