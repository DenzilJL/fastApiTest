
from pydantic import BaseModel, EmailStr
from datetime import datetime


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


class Token (BaseModel):
    access_token: str
    token_tyoe: str


class TokenData (BaseModel):
    id: int


class Post (BaseModel):
    title: str
    description: str
    published: bool = True
    owner_id: int


class PostResp (Post):
    id: int
    created_at: datetime
    owner: UserBase

    class Config:
        orm = True
