from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LikeDislikeCreate, LikeDislikeUpdate
from app.models import LikeDislike


async def create_like_or_dislike(db: AsyncSession, like_dislike: LikeDislikeCreate):
    new_like_dislike = LikeDislike(
        user_id=like_dislike.user_id,
        post_id=like_dislike.post_id,
        like=like_dislike.like,
        dislike=like_dislike.dislike
    )
    db.add(new_like_dislike)
    await db.commit()
    return new_like_dislike


async def get_count_like(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(func.count())
        .select_from(LikeDislike)
        .where(LikeDislike.like==True)
        .where(LikeDislike.post_id==post_id)
    )
    return result.scalar()


async def get_count_dislike(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(func.count())
        .select_from(LikeDislike)
        .where(LikeDislike.dislike==True)
        .where(LikeDislike.post_id==post_id)
    )
    return result.scalar()


async def get_like_dislike(db: AsyncSession, post_id: int, user_id: int):
    result = await db.execute(
        select(LikeDislike)
        .where(LikeDislike.user_id==user_id)
        .where(LikeDislike.post_id==post_id)
    )
    return result.scalars().first()


async def update_like_or_dislike(
    db: AsyncSession, 
    new_like_dislike: LikeDislikeUpdate, 
    like_dislike: LikeDislike
):
    if new_like_dislike.like:
        like_dislike.like = new_like_dislike.like
        like_dislike.dislike = False
    else:
        like_dislike.dislike = new_like_dislike.dislike
        like_dislike.like = False
    await db.commit()
    return like_dislike


async def delete_like_or_dislike(db: AsyncSession, post_id: int, user_id: int):
    await db.execute(
        delete(LikeDislike)
        .where(LikeDislike.user_id==user_id)
        .where(LikeDislike.post_id==post_id)
    )
    await db.commit()
    return True