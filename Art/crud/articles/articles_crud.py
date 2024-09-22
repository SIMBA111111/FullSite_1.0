import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update, func, and_

from models.users.user_model import UserModel
from models.articles.articles_model import ArticleModel
from schemas.articles.articles_schemas import SSlug


def get_article_by_id(db: Session, article_id: int):
    return db.query(ArticleModel).filter(ArticleModel.id == article_id).first()


async def get_article_by_slug(db: AsyncSession, slug: SSlug):
    result = await db.execute(select(ArticleModel).filter(ArticleModel.slug == slug.slug))
    return result.scalars().first()


async def update_count_views_by_article(db: AsyncSession, new_count_views: int, slug: SSlug):
    await db.execute(update(ArticleModel)
        .where(ArticleModel.slug == slug.slug)
        .values(count_views=new_count_views)
    )
    await db.commit()


def get_article_by_name(db: Session, article_name: str):
    return db.query(ArticleModel).filter(ArticleModel.name == article_name).first()


def get_articles(db: Session, skip: int = 0, limit: int = 20):
    return db.query(ArticleModel).offset(skip).limit(limit).all()


async def create_article(db: AsyncSession, name: str, intro_text: str, author: UserModel, title: str):
    db_item = ArticleModel(title=title.lower(), name=name, intro_text=intro_text, user=author)
    rand = random.randint(a=10000000, b=99999999)
    db_item.slug = f"{db_item.name}-{rand}"
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_all_articles(db: AsyncSession, page: int):
    result = await db.execute(
        select(ArticleModel, UserModel.first_name, UserModel.last_name, UserModel.username)
        .join(ArticleModel.user)
        .filter(
            and_(
                ArticleModel.bid_approved == True,
                ArticleModel.disable == False
            )
        )
        .offset((page - 1) * 6)
        .limit(6)
    )
    return result.all()
    # return result.scalars().all()


async def get_last_article(db: AsyncSession):
    result = await db.execute(select(ArticleModel).order_by(ArticleModel.id.desc()))
    return result.scalars().first()


async def get_titles_articles(db: AsyncSession, article_title: str):
    result = await db.execute(select(ArticleModel.title)
        .filter(
            and_(
                ArticleModel.title.like(f"%{article_title.lower()}%"),
                ArticleModel.disable == False
            )
        )
    )
    return result.scalars().all()


async def get_articles_by_title(article_title: str, db: AsyncSession, page: int):
    result = await db.execute(
        select(ArticleModel, UserModel.first_name, UserModel.last_name, UserModel.username)
        .join(ArticleModel.user)
        .filter(
            and_(
                ArticleModel.title.ilike(f"%{article_title}%"),
                ArticleModel.bid_approved == True,
                ArticleModel.disable == False
            )
        )
        .offset((page - 1) * 6)
        .limit(6)
    )

    return result.all()

