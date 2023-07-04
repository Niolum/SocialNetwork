from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post
from app.schemas import PostCreate, PostUpdate


async def create_post(db: AsyncSession, post: PostCreate):
    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=post.owner_id
    )
    db.add(new_post)
    await db.commit()
    return new_post


async def get_post_by_title(db: AsyncSession, title: str):
    result = await db.execute(
        select(Post)
        .where(Post.title==title)
        .options(selectinload(Post.owner))
    )
    return result.scalars().first()


async def get_post_by_id(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(Post)
        .where(Post.id==post_id)
        .options(selectinload(Post.owner))
    )
    return result.scalars().first()


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Post)
        .order_by(Post.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Post.owner))
    )
    return result.scalars().fetchall()


async def update_post(db: AsyncSession, post: Post, new_post: PostUpdate):
    if new_post.title:
        post.title = new_post.title
    if new_post.content:
        post.content = new_post.content
    await db.commit()
    return post


async def is_users_post(db: AsyncSession, post_id: int, owner_id: int):
    result = await db.execute(
        select(Post)
        .where(Post.id==post_id)
        .where(Post.owner_id==owner_id)
        .options(selectinload(Post.owner))
    )
    return result.scalars().first()


async def delete_post(db: AsyncSession, post_id: int):
    await db.execute(
        delete(Post)
        .where(Post.id==post_id)
    )
    await db.commit()
    return True