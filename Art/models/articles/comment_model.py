import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base_model import BaseModel

# if TYPE_CHECKING:
# from models.articles.articles_model import ArticleModel
# from models.users.user_model import UserModel


class CommentModel(BaseModel):

    __tablename__ = 'comment'

    content: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("article.id"))

    user: Mapped["UserModel"] = relationship(back_populates="comments")
    article: Mapped["ArticleModel"] = relationship(back_populates="comments")
