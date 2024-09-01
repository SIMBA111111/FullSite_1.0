from sqlalchemy.orm import Session

from models.articles.articles_model import ArticleModel
from schemas.admin.admin_schemas import FileDownloadRequest


def get_bid_list(db: Session):
    bid_list = (
        db.query(ArticleModel)
        .with_entities(
            ArticleModel.id,
            ArticleModel.name,
            ArticleModel.bid_approved,
            ArticleModel.intro_text,
        )
        .filter(ArticleModel.bid_approved == False)
        .all()
    )
    return bid_list


def approve_bid(db: Session, filename: FileDownloadRequest):
    approved_article = db.query(ArticleModel).filter(ArticleModel.name == filename.filename).first()
    approved_article.bid_approved = True
    db.commit()
    db.refresh(approved_article)


def delete_bid(db: Session, filename: FileDownloadRequest):
    article = db.query(ArticleModel).filter(ArticleModel.name == filename.filename).first()
    db.delete(article)
    db.commit()