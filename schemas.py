import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UsernameChangeSchema(BaseModel):
    name: str


class PasswordChangeSchema(BaseModel):
    password: str
    new_password: str


class PostCreateSchema(BaseModel):
    title: str
    content: str


class PostUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class CommentCreateSchema(BaseModel):
    post_id: int
    comment: str


class CommentUpdateSchema(BaseModel):
    comment_id: int
    comment: str


class LikeCreatSchema(BaseModel):
    post_id: int
