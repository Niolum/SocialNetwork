from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User
from app.schemas import Post, PostCreate, PostUpdate
from app.crud import (
    create_post,
    get_post_by_title,
    get_post_by_id,
    get_posts,
    update_post,
    is_users_post,
    delete_post
)
from app.oauth2 import get_current_user


post_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@post_router.post("/", response_model=Post)
async def create_new_post(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    post: PostCreate
):
    db_post = await get_post_by_title(db=db, title=post.title)
    if db_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already a Post with this title"
        )
    if current_user.id != post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="owner_id must be equal to the id of the current user"
        )
    new_post = await create_post(db=db, post=post)
    return new_post


@post_router.get("/{post_id}", response_model=Post)
async def get_post(
    db: Annotated[AsyncSession, Depends(get_session)],
    post_id: int
):
    post = await get_post_by_id(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not Found"
        )
    return post


@post_router.get("/", response_model=list[Post])
async def get_all_posts(
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100
):
    posts = await get_posts(db=db, skip=skip, limit=limit)
    return posts


@post_router.put("/{post_id}", response_model=Post)
async def change_post_data(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    post_id: int,
    new_post: PostUpdate
):
    if current_user.id != new_post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="owner_id must be equal to the id of the current user"
        )
    post_db = await is_users_post(db=db, post_id=post_id, owner_id=current_user.id)
    if post_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The post must be owned by the current user"
        )
    post = await update_post(db=db, post=post_db, new_post=new_post)
    return post


@post_router.delete("/{post_id}")
async def remove_post(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    post_id: int
):
    post_db = await is_users_post(db=db, post_id=post_id, owner_id=current_user.id)
    if post_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The post must be owned by the current user"
        )
    
    await delete_post(db=db, post_id=post_id)
    data = {"message": "Post has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)