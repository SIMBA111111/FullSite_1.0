from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base_model import BaseModel


class CommentModel(BaseModel):

    __tablename__ = 'comment'

    content: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("article.id"))

    user: Mapped["UserModel"] = relationship(back_populates="comments")
    article: Mapped["ArticleModel"] = relationship(back_populates="comments")
