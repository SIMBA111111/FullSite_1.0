from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import func, select

from models.articles.articles_model import ArticleModel
from models.users.user_model import UserModel


async def get_all_authors(db: AsyncSession):
    result = await db.execute(
        select(
            UserModel,
            func.sum(ArticleModel.count_views).label('views_count'),
            func.min(ArticleModel.created_at).label('first_article_date')
        )
        .join(ArticleModel, UserModel.id == ArticleModel.user_id)
        .group_by(UserModel.id)
        .order_by(func.sum(ArticleModel.count_views).desc())
    )
    users_ordered_by_article_count = result.all()
    return users_ordered_by_article_count
