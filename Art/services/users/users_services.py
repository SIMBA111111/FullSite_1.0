from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from config.log_config import logger
from crud.auth import auth_crud
from crud.users import users_crud
from models.users import UserModel
from models.users.user_model import AnonymousUser
from schemas.users.users_schemas import SUserBase, SAuthorsList, SUsername
from services.auth import auth_services


def create_user(db: Session, item: SUserBase):
    hashed_password = users_crud.hash_password(item["password"])
    item["password"] = hashed_password
    if isinstance(item, SUserBase):
        new_user = UserModel(**item.dict())
    else:
        new_user = UserModel(**item)
    try:
        auth_crud.create_user(db, new_user)
    except Exception as e:
        logger.error(f"Failed to create a new user. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Failed to create a new user. Error: {e}"})
    return new_user


def get_all_authors(db: Session):
    try:
        users_ordered_by_article_count = users_crud.get_all_authors(db)
    except Exception as e:
        logger.error(f"Couldn't get all the authors. Error: {e}")
        raise HTTPException(status_code=400, detail={"message": f"Couldn't get all the authors. Error: {e}"})

    users_ordered_by_article_count_response = [
        SAuthorsList(
            id=author[0].id,
            first_name=author[0].first_name,
            last_name=author[0].last_name,
            email=author[0].email,
            username=author[0].username,
        )
        for author in users_ordered_by_article_count
    ]

    return users_ordered_by_article_count_response


def get_author(db: Session, username: SUsername):
    author = auth_services.get_user_by_username(db, username.username)
    author = SAuthorsList(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        email=author.email,
        username=author.username
    )
    author_response = jsonable_encoder(author)

    return author_response


def user_or_anonym(current_user: UserModel | AnonymousUser):
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
