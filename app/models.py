from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column, MappedAsDataclass, DeclarativeBase


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True)
    }
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    content: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())

    owner: Mapped["User"] = relationship("User")


class LikeDislike(Base):
    __tablename__ = "like_dislike"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)
    like: Mapped[bool] = mapped_column(default=False)
    dislike: Mapped[bool] = mapped_column(default=False)