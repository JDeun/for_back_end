from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    author_id: str
    llm_id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True
