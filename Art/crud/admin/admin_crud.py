from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.articles.articles_model import ArticleModel
from models.users import UserModel
from schemas.admin.admin_schemas import FileDownloadRequest


async def get_bid_list(db: AsyncSession):
    result = await db.execute(
        select(
            ArticleModel.id,
            ArticleModel.name,
            ArticleModel.bid_approved,
            ArticleModel.intro_text,
        )
        .filter(ArticleModel.bid_approved == False)
    )

    bid_list = result.fetchall()
    return bid_list


async def approve_bid(db: AsyncSession, filename: FileDownloadRequest):
    result = await db.execute(select(ArticleModel).filter(ArticleModel.name == filename.filename))
    approved_article = result.scalars().first()
    approved_article.bid_approved = True
    await db.commit()
    await db.refresh(approved_article)


async def delete_bid(db: AsyncSession, filename: FileDownloadRequest):
    result = await db.execute(select(ArticleModel).filter(ArticleModel.name == filename.filename))
    article = result.scalars().first()
    await db.delete(article)
    await db.commit()


async def disable_article(db: AsyncSession, article: ArticleModel, disable: bool):
    article.disable = disable
    await db.commit()


async def get_all_articles(db: AsyncSession, page: int):
    result = await db.execute(
        select(ArticleModel, UserModel.first_name, UserModel.last_name, UserModel.username)
        .join(ArticleModel.user)
        .filter(
                ArticleModel.bid_approved == True,
        )
        .offset((page - 1) * 2)
        .limit(2)
    )
    return result.all()