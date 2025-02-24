
from pydantic import BaseModel,EmailStr
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
    email: EmailStr

    active: bool = True


class User (UserBase):
    password: str


class UserResp (UserBase):
    id: int
    created_at: datetime

    class Config:
        orm = True

class UserLogin (BaseModel):
    email: EmailStr
    password: str