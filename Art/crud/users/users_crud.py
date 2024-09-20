from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.concurrency import run_in_threadpool

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from models.articles.articles_model import ArticleModel
from models.users.user_model import UserModel

from schemas.users.users_schemas import SUserBase


async def get_all_authors(db: AsyncSession):
    result = await db.execute(
        select(UserModel, func.sum(ArticleModel.count_views).label('views_count'))
        .join(ArticleModel, UserModel.id == ArticleModel.user_id)
        .group_by(UserModel.id)
        .order_by(func.sum(ArticleModel.count_views).desc())
    )
    users_ordered_by_article_count = result.all()
    return users_ordered_by_article_count
