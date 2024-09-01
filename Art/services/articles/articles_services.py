from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from transliterate import translit

from config.log_config import logger

import os

from schemas.articles.articles_schemas import SSlug

from crud.articles import articles_crud


def translate_ru_in_en(file: UploadFile) -> str:
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
        logger.error(f"The title of the article could not be translated. Error: {e}")
        raise HTTPException(status_code=400,
                            detail={"Error": f"The title of the article could not be translated. Error: {e}"}
                            )
    return filename


def create_new_article_name(article_last, filename: str) -> str:
    try:
        if article_last is None:
            new_article_name = f"1_{filename}"
        else:
            new_article_name = f"{article_last.id + 1}_{filename}"
    except Exception as e:
        logger.error(f"Failed to create a new article title. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Failed to create a new article title. Error: {e}"})
    return new_article_name


def write_file(new_article_name: str, file: UploadFile):
    try:
        file_path = os.path.join(os.getcwd(), "articles_list", new_article_name)

        with open(file_path, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        logger.error(f"The file could not be written. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"There was an error uploading the file. Error: {e}"})
    finally:
        file.file.close()


def get_article(db: Session, slug: SSlug):
    try:
        filename = articles_crud.get_article_by_slug(db, slug)
    except Exception as e:
        logger.error(f"The article could not be retrieved by slug. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"Error": f"The article could not be retrieved by slug. Error: {str(e)}"}
        )

    file_ = f"{filename.name[:-5]}.html"
    file_path = os.path.join(os.getcwd(), "static", "articles", filename.name[:-5], file_)

    try:
        with open(file_path, "r", encoding='utf-8') as file:
            file_content = file.read()
    except Exception as e:
        logger.error(f"The file could not be opened: {file_}. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"Error": f"The file could not be opened: {str(e)}"}
        )

    new_count_views = filename.count_views + 1
    try:
        articles_crud.update_count_views_by_article(db, new_count_views, slug)
    except Exception as e:
        logger.error(f"The number of article views could not be updated. Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"Error": f"The number of article views could not be updated: {str(e)}"}
        )

    return file_content


def get_all_articles(db: Session):
    try:
        all_articles = articles_crud.get_all_articles(db)
    except Exception as e:
        logger.error(f"Couldn't get all the articles. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get all the articles. Error: {e}"})
    return all_articles


def get_last_article(db: Session):
    try:
        last_article = articles_crud.get_last_article(db)
    except Exception as e:
        logger.error(f"Couldn't get the latest article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get the latest article. Error: {e}"})
    return last_article
