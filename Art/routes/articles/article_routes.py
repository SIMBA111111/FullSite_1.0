from fastapi import APIRouter, UploadFile, File, Body, Depends, Header
from fastapi.responses import UJSONResponse, Response, JSONResponse
from sqlalchemy.orm import Session

from dependencies import get_db
from config.log_config import logger

from models.articles.articles_model import ArticleModel
from models.users import UserModel

from services.articles import articles_services

from services.auth.auth_services import get_current_user

from schemas.articles.articles_schemas import SSlug, SArticleListWithAuthors

from crud.articles import articles_crud

router = APIRouter()


@router.post("/create", summary="Create new article")
def create_article(
                    file: UploadFile = File(),
                    name: str = Body(),
                    intro_text: str = Body(),
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user),
                    ):
    logger.info(f" - {current_user.username} - START create_article")

    article_last = articles_services.get_last_article(db)

    filename = articles_services.translate_ru_in_en(file)
    new_article_name = articles_services.create_new_article_name(article_last, filename)
    articles_services.write_file(new_article_name, file)
    articles_crud.create_article(db, new_article_name, intro_text, current_user)

    response = JSONResponse(status_code=201, content={"Success": "Article created"})
    logger.info(f" - {current_user.username} - SUCCESS create_article")
    return response


@router.get("/get-all-articles",
            response_model=list[SArticleListWithAuthors],
            summary="Get all articles"
            )
def get_all_articles(db: Session = Depends(get_db),
                     current_user: UserModel = Depends(get_current_user),
                     ):
    logger.info(f" - {current_user.username} - START get-all-articles")

    all_articles = articles_services.get_all_articles(db)

    # response = JSONResponse(content={"items": all_articles})
    logger.info(f" - {current_user.username} - SUCCESS get-all-articles")
    # return response
    return all_articles


@router.post("/get-article", summary="Get article")
def get_article(slug: SSlug = Body(),
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user),
                ):
    logger.info(f" - {current_user.username} - START get_article")

    file_content = articles_services.get_article(db, slug)

    response = JSONResponse(content={"file_content": file_content}, headers=
                            {"Content-Type": "application/json; charset=utf-8"})
    logger.info(f" - {current_user.username} - SUCCESS get_article")
    return response
