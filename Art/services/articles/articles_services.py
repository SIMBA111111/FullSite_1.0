from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from transliterate import translit

from config.log_config import error_logger

import os
import aiofiles

from schemas.articles.articles_schemas import SSlug, SArticleListWithAuthors

from crud.articles import articles_crud
from schemas.users.users_schemas import SAuthorsList


async def translate_ru_in_en(file: UploadFile) -> str:
    try:
        england_filename = translit(file.filename, language_code='ru', reversed=True)
        filename = ""
        if " " in england_filename:
            england_words_list = england_filename.split(" ")
            filename = ""
            for england_word in england_words_list:
                filename += england_word
                if ".doc" in england_word:
                    break
                filename += "_"
        else:
            filename = england_filename
    except Exception as e:
        error_logger.error(f"The title of the article could not be translated. Error: {e}")
        raise HTTPException(status_code=400,
                            detail={"Error": f"The title of the article could not be translated. Error: {e}"}
                            )
    return filename


async def create_new_article_name(article_last, filename: str) -> str:
    try:
        if article_last is None:
            new_article_name = f"1_{filename}"
        else:
            new_article_name = f"{article_last.id + 1}_{filename}"
    except Exception as e:
        error_logger.error(f"Failed to create a new article title. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Failed to create a new article title. Error: {e}"})
    return new_article_name


async def write_file(new_article_name: str, file: UploadFile):
    try:
        file_path = os.path.join(os.getcwd(), "articles_list", new_article_name)

        async with aiofiles.open(file_path, 'wb') as f:
            while contents := await file.read(1024 * 1024):
                await f.write(contents)
    except Exception as e:
        error_logger.error(f"The file could not be written. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"There was an error uploading the file. Error: {e}"})
    finally:
        await file.close()


async def get_article(db: AsyncSession, slug: SSlug):
    try:
        filename = await articles_crud.get_article_by_slug(db, slug)
    except Exception as e:
        error_logger.error(f"The article could not be retrieved by slug. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"Error": f"The article could not be retrieved by slug. Error: {str(e)}"}
        )

    file_ = f"{filename.name[:-5]}.html"
    file_path = os.path.join(os.getcwd(), "static", "articles", filename.name[:-5], file_)
    try:
        async with aiofiles.open(file_path, "r", encoding='utf-8') as file:
            file_content = await file.read()
    except Exception as e:
        error_logger.error(f"The file could not be opened: {file_}. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"Error": f"The file could not be opened: {str(e)}"}
        )

    new_count_views = filename.count_views + 1
    try:
        await articles_crud.update_count_views_by_article(db, new_count_views, slug)
    except Exception as e:
        error_logger.error(f"The number of article views could not be updated. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"Error": f"The number of article views could not be updated: {str(e)}"}
        )

    return file_content


async def get_all_articles(db: AsyncSession, page: int):
    try:
        all_articles = await articles_crud.get_all_articles(db, page)
    except Exception as e:
        error_logger.error(f"Couldn't get all the articles. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get all the articles. Error: {e}"})

    try:
        articles = []
        for article, first_name, last_name, username in all_articles:
            article_with_author = SArticleListWithAuthors(
                name=article.name,
                intro_text=article.intro_text,
                slug=article.slug,
                count_views=article.count_views,
                title=article.title,
                date=article.created_at,
                user=SAuthorsList(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                )
            )
            articles.append(article_with_author)
    except Exception as e:
        error_logger.error(f"Couldn't serialize all the articles. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't serialize all the articles. Error: {e}"})

    return articles


async def get_last_article(db: AsyncSession):
    try:
        last_article = await articles_crud.get_last_article(db)
    except Exception as e:
        error_logger.error(f"Couldn't get the latest article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get the latest article. Error: {e}"})
    return last_article


async def get_titles_articles(db: AsyncSession, query: str):
    try:
        articles = await articles_crud.get_titles_articles(db, query)
    except Exception as e:
        error_logger.error(f"Couldn't get the title article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get the title article. Error: {e}"})

    return articles


async def get_articles_by_title(article_title: str,
                                db: AsyncSession,
                                page: int):
    try:
        articles = await articles_crud.get_articles_by_title(article_title, db, page)
    except Exception as e:
        error_logger.error(f"Couldn't get the articles by title. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get the articles by title. Error: {e}"})

    try:
        articles_response = []
        for article, first_name, last_name, username in articles:
            _article = SArticleListWithAuthors(
                name=article.name,
                intro_text=article.intro_text,
                slug=article.slug,
                count_views=article.count_views,
                date=article.created_at,
                title=article.title,
                user=SAuthorsList(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                )
            )
            articles_response.append(_article)
    except Exception as e:
        error_logger.error(f"Couldn't serialize the articles by title. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't serialize the articles by title. Error: {e}"})

    return articles_response
