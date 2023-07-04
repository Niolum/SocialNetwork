from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.oauth2 import get_current_user
from app.database import get_session
from app.schemas import LikeDislike, LikeDislikeCreate, LikeCount, DislikeCount, LikeDislikeUpdate
from app.crud import (
    create_like_or_dislike, 
    is_users_post, 
    get_post_by_id,
    get_count_like,
    get_count_dislike,
    update_like_or_dislike,
    get_like_dislike,
    delete_like_or_dislike
)
from app.models import User
from app.exceptions import Exception_404, ExceptionOwnerUserID, ExceptionEqualLikeDislike


like_dislike_router = APIRouter(
    prefix="/likes_dislikes",
    tags=["likes_dislikes"],
    responses={404: {"description": "Not found"}},
)


@like_dislike_router.post("/", response_model=LikeDislike)
async def create_new_like_or_dislike(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    new_like_or_dislike: LikeDislikeCreate
):
    post_db = await is_users_post(
        db=db, 
        post_id=new_like_or_dislike.post_id, 
        owner_id=new_like_or_dislike.user_id
    )
    if post_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't like or dislike your post"
        )
    
    if current_user.id != new_like_or_dislike.user_id:
        raise ExceptionOwnerUserID(name="user_id")
    
    post_db = await get_post_by_id(db=db, post_id=new_like_or_dislike.post_id)
    if post_db is None:
        raise Exception_404(name="Post")
    
    like_dislike_db = await get_like_dislike(db=db, post_id=new_like_or_dislike.post_id, user_id=new_like_or_dislike.user_id)
    if like_dislike_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Like or Dislike already exists"
        )
    
    if (new_like_or_dislike.like and new_like_or_dislike.dislike) or (new_like_or_dislike.like==False and new_like_or_dislike.dislike==False):
        raise ExceptionEqualLikeDislike
    
    like_or_dislike = await create_like_or_dislike(db=db, like_dislike=new_like_or_dislike)
    return like_or_dislike


@like_dislike_router.get("/like/{post_id}", response_model=LikeCount)
async def get_likes(
    db: Annotated[AsyncSession, Depends(get_session)],
    post_id: int
):
    post_db = await get_post_by_id(db=db, post_id=post_id)
    if post_db is None:
        raise Exception_404(name="Post")
    
    count = await get_count_like(db=db, post_id=post_id)
    data = {"likes": count}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@like_dislike_router.get("/dislike/{post_id}", response_model=DislikeCount)
async def get_dislikes(
    db: Annotated[AsyncSession, Depends(get_session)],
    post_id: int
):
    post_db = await get_post_by_id(db=db, post_id=post_id)
    if post_db is None:
        raise Exception_404(name="Post")
    
    count = await get_count_dislike(db=db, post_id=post_id)
    data = {"dislikes": count}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@like_dislike_router.put("/{post_id}", response_model=LikeDislike)
async def change_like_dislike(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    new_like_or_dislike: LikeDislikeUpdate,
    post_id: int
):
    post_db = await get_post_by_id(db=db, post_id=post_id)
    if post_db is None:
        raise Exception_404(name="Post")
    
    like_dislike = await get_like_dislike(db=db, post_id=post_id, user_id=current_user.id)
    if like_dislike is None:
        raise Exception_404(name="Like or Dislike")
    
    if (new_like_or_dislike.like and new_like_or_dislike.dislike) or (new_like_or_dislike.like==False and new_like_or_dislike.dislike==False):
        raise ExceptionEqualLikeDislike
    
    like_dislike = await update_like_or_dislike(
        db=db, 
        new_like_dislike=new_like_or_dislike, 
        like_dislike=like_dislike
    )
    return like_dislike


@like_dislike_router.delete("/{post_id}")
async def remove_like_or_dislike(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    post_id: int
):
    post_db = await get_post_by_id(db=db, post_id=post_id)
    if post_db is None:
        raise Exception_404(name="Post")
    
    like_dislike = await get_like_dislike(db=db, post_id=post_id, user_id=current_user.id)
    if like_dislike is None:
        raise Exception_404(name="Like or Dislike")
    
    await delete_like_or_dislike(db=db, post_id=post_id, user_id=current_user.id)
    data = {"message": "Like or Dislike has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)