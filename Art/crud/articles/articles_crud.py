import random

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from models.users.user_model import UserModel
from models.articles.articles_model import ArticleModel
from schemas.articles.articles_schemas import SSlug


def get_article_by_id(db: Session, article_id: int):
    return db.query(ArticleModel).filter(ArticleModel.id == article_id).first()


def get_article_by_slug(db: Session, slug: SSlug):
    return db.query(ArticleModel).filter(ArticleModel.slug == slug.slug).first()


def update_count_views_by_article(db: Session, new_count_views: int, slug: SSlug):
    db.execute(update(ArticleModel)
               .where(ArticleModel.slug == slug.slug)
               .values(count_views=new_count_views)
               )
    db.commit()


def get_article_by_name(db: Session, article_name: str):
    return db.query(ArticleModel).filter(ArticleModel.name == article_name).first()


def get_articles(db: Session, skip: int = 0, limit: int = 20):
    return db.query(ArticleModel).offset(skip).limit(limit).all()


def create_article(db: Session, name: str, intro_text: str, author_id: int, title: str):
    db_item = ArticleModel(title=title, name=name, intro_text=intro_text, user=author_id)
    rand = random.randint(a=10000000, b=99999999)
    db_item.slug = f"{db_item.name}-{rand}"
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_articles(db: Session, page: int):
    return (db.execute(
            select(ArticleModel, UserModel.first_name, UserModel.last_name, UserModel.username)
            .join(ArticleModel.user)
            .options(joinedload(ArticleModel.user))
            .where(ArticleModel.bid_approved == True)
            .offset((page - 1) * 2)  # Смещение, основанное на номере страницы
            .limit(2)          # Ограничение количества записей на страницу
        )
        .all()
    )


def get_last_article(db: Session):
    return db.query(ArticleModel).order_by(ArticleModel.id.desc()).first()


def get_titles_articles(db: Session):
    return db.scalars(select(ArticleModel.title)).all()
