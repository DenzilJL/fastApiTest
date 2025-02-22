
from pydantic import BaseModel
from datetime import datetime


class Post (BaseModel):
    title: str
    description: str
    published: bool = True


class PostResp (Post):
    id: int
    created_at: datetime

    class Config:
        orm = True


class UserBase (BaseModel):
    user_name: str
    email: str

    active: bool = True


class User (UserBase):
    password: str


class UserResp (UserBase):
    id: int
    created_at: datetime

    class Config:
        orm = True
