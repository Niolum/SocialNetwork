from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    email: str


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    owner_id: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner: User


class LikeDislikeBase(BaseModel):
    user_id: int
    post_id: int
    like: bool | None
    dislike: bool | None

class LikeDislike(LikeDislikeBase):
    id: int