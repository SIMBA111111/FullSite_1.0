from typing import List, Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base_model import BaseModel


class UserModel(BaseModel):

    __tablename__ = 'user'

    first_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_admin_user: Mapped[bool] = mapped_column(Boolean, default=False)

    comments: Mapped[List["CommentModel"]] = relationship(back_populates="user")
    articles: Mapped[List["ArticleModel"]] = relationship(back_populates="user")


class AnonymousUser(BaseModel):

    __tablename__ = 'AnonymousUser'

    username: Mapped[str] = mapped_column(String, unique=True, default="AnonymousUser")
