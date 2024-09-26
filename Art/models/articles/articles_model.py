from typing import List
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base_model import BaseModel

from models.users.user_model import UserModel


class ArticleModel(BaseModel):

    __tablename__ = 'article'

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True)
    intro_text: Mapped[str] = mapped_column(String(70))
    bid_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    count_views: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    disable: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["UserModel"] = relationship(back_populates="articles")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="article")
