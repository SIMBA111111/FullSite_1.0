import urllib

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

import os
import subprocess
import aiofiles

from config.log_config import info_logger, error_logger

from models.users import UserModel
from models.users.user_model import AnonymousUser

from schemas.admin.admin_schemas import FileDownloadRequest, BidListResponseModel

from crud.admin import admin_crud
from crud.articles import articles_crud
from schemas.articles.articles_schemas import SSlug, SArticleListWithAuthors
from schemas.users.users_schemas import SAuthorsList

host = os.getenv("HOST")


async def get_bid_list(db: AsyncSession):
    try:
        bid_list = await admin_crud.get_bid_list(db)
    except Exception as e:
        error_logger.error(f"Couldn't get a list of articles. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get a list of articles: {str(e)}"})

    bid_list_response = [
        BidListResponseModel(
            id=item.id,
            name=item[1],
            bid_approved=item[2],
            intro_text=item[3],
        )
        for item in bid_list
    ]

    return bid_list_response


async def create_html_file(filename: FileDownloadRequest) -> str:
    try:
        dir_path = f"static/articles/{filename.filename[:-5]}"
        os.makedirs(dir_path, exist_ok=True)

        command = f'mammoth "articles_list/{filename.filename}" --output-dir="{dir_path}"'
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        if result.returncode != 0:
            error_logger.error(f"Mammoth conversion failed: {result.stderr}")
            raise Exception(f"Mammoth command failed with exit status {result.returncode}: {result.stderr}")

    except subprocess.CalledProcessError as e:
        error_logger.error(f"Mammoth conversion error: {e.stderr}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e.stderr)}"})
    except Exception as e:
        error_logger.error(f"The file {filename.filename} could not be converted to html. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e)}"})

    html_file_name = f"{filename.filename[:-5]}" + ".html"
    return html_file_name


async def create_paths_in_src_in_html_files(filename: FileDownloadRequest, html_file_name: str):
    file_path = os.path.join(os.getcwd(), "static", "articles", filename.filename[:-5], html_file_name)

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
            file_content = await file.read()
    except Exception as e:
        error_logger.error(f"The file could not be opened {html_file_name}. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error opening the file: {str(e)}"})

    new_img_path = f'/static/articles/{filename.filename[:-5]}/'
    updated_content = file_content.replace('<img src="', f'<img src="{new_img_path}')

    try:
        async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
            await file.write(updated_content)
    except Exception as e:
        error_logger.error(f"Error when rewriting the file {html_file_name}. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error rewriting the file: {str(e)}"})


async def approve_article_bid_approved(filename: FileDownloadRequest, db: AsyncSession):
    try:
        await admin_crud.approve_bid(db, filename)
    except Exception as e:
        error_logger.error(f"Error in approving the article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e)}"})


async def cancel_bid(db: AsyncSession, filename: FileDownloadRequest):
    try:
        await admin_crud.delete_bid(db, filename)
        os.remove(f"articles_list/{filename.filename}")
    except Exception as e:
        error_logger.error(f"Error when canceling an article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error when canceling an article: {str(e)}"})


async def process_html_file(html_file_name, output_file):
    input_file_path = os.path.join(os.getcwd(), "static", "articles", html_file_name[:-5], html_file_name)
    output_file_path = os.path.join(os.getcwd(), "static", "articles", output_file[:-5], output_file)

    async with aiofiles.open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = await file.read()

    new_html_content = ""

    while new_html_content != html_content:
        html_content = html_content.replace('<p>!@#$</p>', '<div class="code">', 1)
        new_html_content = html_content

        html_content = new_html_content.replace('<p>!@#$</p>', '</div>', 1)

    async with aiofiles.open(output_file_path, 'w', encoding='utf-8') as file:
        await file.write(new_html_content)


async def path_to_file(filename: FileDownloadRequest):
    try:
        decoded_filename = urllib.parse.unquote(filename.filename)
        path = os.path.join(os.getcwd(), "articles_list", decoded_filename)
    except Exception as e:
        error_logger.error(f"Error in getting the article path. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in getting the article path: {str(e)}"})
    return path


async def check_is_admin_user(current_user: UserModel | AnonymousUser):
    if current_user is None:
        raise HTTPException(status_code=403, detail={"Error": "You need to login"})
    if isinstance(current_user, AnonymousUser):
        raise HTTPException(status_code=403, detail={"Error": "You need to login"})
    if current_user.is_admin_user is not True:
        raise HTTPException(status_code=403, detail={"Error": "Login with an administrator account"})
    return 200


async def disable_article(db: AsyncSession, disable: bool, slug: SSlug):
    try:
        article = await articles_crud.get_article_by_slug(db, slug)
        await admin_crud.disable_article(db, article, disable)
    except Exception as e:
        error_logger.error(f"Error hiding the article: Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error hiding the article: {str(e)}"})
    return article


async def get_all_articles(db: AsyncSession, page: int):
    try:
        all_articles = await admin_crud.get_all_articles(db, page)
    except Exception as e:
        error_logger.error(f"Error get all articles in admin panel: Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error get all articles in admin panel: {str(e)}"})

    try:
        articles = []
        for article, first_name, last_name, username in all_articles:
            article_with_author = SArticleListWithAuthors(
                name=article.name,
                intro_text=article.intro_text,
                slug=article.slug,
                count_views=article.count_views,
                title=article.title,
                user=SAuthorsList(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                )
            )
            articles.append(article_with_author)
    except Exception as e:
        error_logger.error(f"Couldn't serialize all the articles in admin panel. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't serialize all the articles. Error: {e}"})

    return articles
