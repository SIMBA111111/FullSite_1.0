from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from config.log_config import error_logger
from crud.auth import auth_crud
from crud.users import users_crud
from models.users import UserModel
from models.users.user_model import AnonymousUser
from schemas.users.users_schemas import SUserBase, SAuthorsList, SUsername
from services.auth import auth_services


async def create_user(db: AsyncSession, item: SUserBase):
    hashed_password = await auth_services.is_hashed_password(item["password"])
    item["password"] = hashed_password
    if isinstance(item, SUserBase):
        new_user = UserModel(**item.dict())
    else:
        new_user = UserModel(**item)
    try:
        await auth_crud.create_user(db, new_user)
    except Exception as e:
        error_logger.error(f"Failed to create a new user. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Failed to create a new user. Error: {e}"})
    return new_user


async def get_all_authors(db: AsyncSession):
    try:
        users_ordered_by_article_count = await users_crud.get_all_authors(db)
    except Exception as e:
        error_logger.error(f"Couldn't get all the authors. Error: {e}")
        raise HTTPException(status_code=400, detail={"message": f"Couldn't get all the authors. Error: {e}"})
    users_ordered_by_article_count_response = [
        SAuthorsList(
            first_name=author.first_name,
            last_name=author.last_name,
            email=author.email,
            username=author.username,
            views_count=views_count,
            first_article_date=first_article_date
        )
        for author, views_count, first_article_date in users_ordered_by_article_count
    ]

    return users_ordered_by_article_count_response


async def get_author(db: AsyncSession, username: SUsername):
    try:
        author = await auth_services.get_user_by_username(db, username.username)
        author = SAuthorsList(
            id=author.id,
            first_name=author.first_name,
            last_name=author.last_name,
            email=author.email,
            username=author.username
        )
        author_response = jsonable_encoder(author)
    except Exception as e:
        error_logger.error(f"Couldn't get the author. Error: {e}")
        raise HTTPException(status_code=400, detail={"message": f"Couldn't get the author. Error: {e}"})

    return author_response


async def user_or_anonym(current_user: UserModel | AnonymousUser):
    data = ""
    if isinstance(current_user, AnonymousUser):
        data = {
            "username": current_user.username,
            "is_admin": False,
        }
    if isinstance(current_user, UserModel):
        data = {
            "username": current_user.username,
            "is_admin": current_user.is_admin_user
        }
    return data
