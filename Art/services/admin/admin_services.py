import urllib
from time import sleep

from sqlalchemy.orm import Session

from fastapi import HTTPException

import os
import subprocess

from config.log_config import logger

from models.users import UserModel
from models.users.user_model import AnonymousUser

from schemas.admin.admin_schemas import FileDownloadRequest, BidListResponseModel

from crud.admin import admin_crud


def get_bid_list(db: Session):
    try:
        bid_list = admin_crud.get_bid_list(db)
    except Exception as e:
        logger.error(f"Couldn't get a list of articles. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't get a list of articles: {str(e)}"})

    bid_list_response = [
        BidListResponseModel(
            id=item[0],
            name=item[1],
            bid_approved=item[2],
            intro_text=item[3],
        )
        for item in bid_list
    ]

    return bid_list_response


def create_html_file(filename: FileDownloadRequest) -> str:
    try:
        dir_path = f"static/articles/{filename.filename[:-5]}"
        os.makedirs(dir_path, exist_ok=True)

        command = f'mammoth "articles_list/{filename.filename}" --output-dir="{dir_path}"'
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Mammoth conversion failed: {result.stderr}")
            raise Exception(f"Mammoth command failed with exit status {result.returncode}: {result.stderr}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Mammoth conversion error: {e.stderr}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e.stderr)}"})
    except Exception as e:
        logger.error(f"The file {filename.filename} could not be converted to html. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e)}"})

    html_file_name = f"{filename.filename[:-5]}" + ".html"
    return html_file_name


def create_paths_in_src_in_html_files(filename: FileDownloadRequest, html_file_name: str):
    try:
        file_path = os.path.join(os.getcwd(), "static", "articles", filename.filename[:-5], html_file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
    except Exception as e:
        logger.error(f"The file could not be opened {html_file_name}. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e)}"})

    updated_content = ''
    pos = 0

    while True:
        start_pos = file_content.find('<img src="', pos)
        if start_pos == -1:
            updated_content += file_content[pos:]
            break

        new_img_path = f'http://127.0.0.1:80/static/articles/{filename.filename[:-5]}/'
        updated_content += file_content[pos:start_pos + 10] + new_img_path
        pos = start_pos + 10

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)
    except Exception as e:
        logger.error(f"Error when rewriting the file {html_file_name}. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e)}"})


def approve_article_bid_approved(filename: FileDownloadRequest, db: Session):
    try:
        admin_crud.approve_bid(db, filename)
    except Exception as e:
        logger.error(f"Error in approving the article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in approving the article: {str(e)}"})


def cancel_bid(db: Session, filename: FileDownloadRequest):
    try:
        admin_crud.approve_bid(db, filename)
        os.remove(f"articles_list/{filename.filename}")
    except Exception as e:
        logger.error(f"Error when canceling an article. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error when canceling an article: {str(e)}"})


def process_html_file(html_file_name, output_file):
    input_file_path = os.path.join(os.getcwd(), "static", "articles", html_file_name[:-5], html_file_name)
    output_file_path = os.path.join(os.getcwd(), "static", "articles", output_file[:-5], output_file)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    new_html_content = ""

    while new_html_content != html_content:
        html_content = html_content.replace('<p>!@#$</p>', '<div class="code">', 1)
        new_html_content = html_content

        html_content = new_html_content.replace('<p>!@#$</p>', '</div>', 1)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(new_html_content)


def path_to_file(filename: FileDownloadRequest):
    try:
        decoded_filename = urllib.parse.unquote(filename.filename)
        path = os.path.join(os.getcwd(), "articles_list", decoded_filename)
    except Exception as e:
        logger.error(f"Error in getting the article path. Ошибка: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Error in getting the article path: {str(e)}"})
    return path


def check_admin_user(current_user: UserModel | AnonymousUser):
    if current_user is None:
        raise HTTPException(status_code=403, detail={"Error": "Login with an administrator account"})
    if isinstance(current_user, AnonymousUser):
        raise HTTPException(status_code=403, detail={"Error": "Login with an administrator account"})
    if current_user.is_admin_user is not True:
        raise HTTPException(status_code=403, detail={"Error": "Login with an administrator account"})
    return 200
