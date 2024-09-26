from fastapi import APIRouter, UploadFile, File, Body, Depends, Form
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from config.log_config import info_logger

from models.users import UserModel

from services.articles import articles_services
from services.auth import auth_services

from services.auth.auth_services import get_current_user

from schemas.articles.articles_schemas import SSlug, SArticleListWithAuthors

from crud.articles import articles_crud

router = APIRouter()


@router.post("/create", summary="Create new article")
async def create_article(file_data: UploadFile = File(...),
                         title: str = Form(...),
                         intro_text: str = Form(...),
                         db: AsyncSession = Depends(get_db),
                         current_user: UserModel = Depends(get_current_user),
                         ):
    info_logger.info(f" - {current_user.username} - START create_article")
    await auth_services.is_authed(current_user)

    article_last = await articles_services.get_last_article(db)

    filename = await articles_services.translate_ru_in_en(file_data)
    new_article_name = await articles_services.create_new_article_name(article_last, filename)
    await articles_services.write_file(new_article_name, file_data)
    await articles_crud.create_article(db, new_article_name, intro_text, current_user, title)

    response = JSONResponse(status_code=201, content={"Success": "Article created"})
    info_logger.info(f" - {current_user.username} - SUCCESS create_article")
    return response


@router.get("/get-all-articles",
            response_model=list[SArticleListWithAuthors],
            summary="Get all articles"
            )
async def get_all_articles(response: Response,
                           page: int = 0,
                           db: AsyncSession = Depends(get_db),
                           current_user: UserModel = Depends(get_current_user),
                           ):
    info_logger.info(f" - {current_user.username} - START get all articles")

    all_articles = await articles_services.get_all_articles(db, page)

    # response = JSONResponse(content={"items": all_articles})
    info_logger.info(f" - {current_user.username} - SUCCESS get all articles")
    # return response
    return all_articles


@router.post("/get-article", summary="Get article")
async def get_article(slug: SSlug = Body(),
                      db: AsyncSession = Depends(get_db),
                      current_user: UserModel = Depends(get_current_user),
                      ):
    info_logger.info(f" - {current_user.username} - START get article")
    file_content = await articles_services.get_article(db, slug)

    response = JSONResponse(content={"file_content": file_content}, headers=
                            {"Content-Type": "application/json; charset=utf-8"})
    info_logger.info(f" - {current_user.username} - SUCCESS get article")
    return response


@router.get("/search-article")
async def search_article(query: str,
                         db: AsyncSession = Depends(get_db)
                         ):
    info_logger.info(f" - START search article")

    data = await articles_services.get_titles_articles(db, query)

    response = JSONResponse(status_code=200, content=data)
    info_logger.info(f" - SUCCESS search article")
    return response


@router.get("/request-articles")
async def request_articles(article_title: str,
                           page: int = 0,
                           db: AsyncSession = Depends(get_db)
                           ):
    info_logger.info(f" - START request articles")

    articles = await articles_services.get_articles_by_title(article_title, db, page)

    info_logger.info(f" - SUCCESS request articles")
    return articles
