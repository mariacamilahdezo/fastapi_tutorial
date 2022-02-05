from os import access
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):

    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Value responses
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


# Models depends on the request


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Likes(BaseModel):
    post_id: int
    dir: conint(le=1)



"""
# The base model is for comments (posts)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default true


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True


class UpdatePost(BaseModel):
    published: bool
"""
