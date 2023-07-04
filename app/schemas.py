from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
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
    owner_id: int


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None
    content: str | None
    owner_id: int


class Post(PostBase):
    id: int
    created_at: datetime
    owner: User


class LikeDislikeBase(BaseModel):
    user_id: int
    post_id: int
    like: bool | None
    dislike: bool | None


class LikeDislikeCreate(LikeDislikeBase):
    pass


class LikeCount(BaseModel):
    likes: int


class DislikeCount(BaseModel):
    dislikes: int


class LikeDislikeUpdate(BaseModel):
    like: bool | None
    dislike: bool | None


class LikeDislike(LikeDislikeBase):
    id: int