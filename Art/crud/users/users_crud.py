from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from models.articles.articles_model import ArticleModel
from models.users.user_model import UserModel

from schemas.users.users_schemas import SUserBase

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_all_authors(db: Session):
    users_ordered_by_article_count = (
        db.query(UserModel, func.count(ArticleModel.id).label('article_count'))
        .join(ArticleModel, UserModel.id == ArticleModel.user_id)
        .group_by(UserModel.id)
        .order_by(func.count(ArticleModel.id).desc())
        .all()
    )
    return users_ordered_by_article_count
