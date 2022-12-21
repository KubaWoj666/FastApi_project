from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = False


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime


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


class Votes(BaseModel):
    post_id: int
    """dir = direction
    conint thanks to this wy can put number les and equal 1 (le=1) unfortunately we can put negative num """
    dir: conint(le=1)

class CommentBase(BaseModel):
    comment: str

class Comment(BaseModel):
    post_id: int
    comment: str


class CommentOut(BaseModel):
    user_id: int
    comment_id: int
    comment: str
    class Config:
        orm_mode = True


class UpdateComment(BaseModel):
    comment: str
    class Config:
        orm_mode = True


class PostsOut(BaseModel):
    Post: PostOut
    likes: int
    comment: Optional[str] = None
    class Config:
        orm_mode = True

