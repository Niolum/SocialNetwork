from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate
from app.utils import get_password_hash


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    return new_user


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(User)
        .where(User.username==username)
    )
    return result.scalars().first()

