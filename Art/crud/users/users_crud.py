from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.concurrency import run_in_threadpool

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from models.articles.articles_model import ArticleModel
from models.users.user_model import UserModel

from schemas.users.users_schemas import SUserBase

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return await run_in_threadpool(pwd_context.hash, password)


async def get_all_authors(db: AsyncSession):
    result = await db.execute(select(UserModel, func.count(ArticleModel.id).label('article_count'))
        .join(ArticleModel, UserModel.id == ArticleModel.user_id)
        .group_by(UserModel.id)
        .order_by(func.count(ArticleModel.id).desc())
    )

    users_ordered_by_article_count = result.fetchall()
    return users_ordered_by_article_count
