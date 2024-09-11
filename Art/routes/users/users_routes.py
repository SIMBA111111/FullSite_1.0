from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from config.log_config import info_logger
from dependencies import get_db
from models.users import UserModel
from schemas.users.users_schemas import SUsername
from services.auth.auth_services import get_current_user
from services.users import users_services

router = APIRouter()


@router.get("/get-all-authors")
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    info_logger.info(f" - START get_all_author")

    users_ordered_by_article_count = await users_services.get_all_authors(db)

    info_logger.info(f" - SUCCESS get_all_authors")
    return users_ordered_by_article_count


@router.post("/get-author")
async def get_author(db: AsyncSession = Depends(get_db),
                     username: SUsername = Body()
                     ):
    info_logger.info("START get_author")

    author = await users_services.get_author(db, username)

    response = JSONResponse(status_code=200, content={"author": author})
    info_logger.info("SUCCESS get_author")
    return response


@router.post("/me")
async def me(current_user: UserModel = Depends(get_current_user)):
    # info_logger.info("START me")

    data = await users_services.user_or_anonym(current_user)

    response = JSONResponse(status_code=200, content={"data": data})
    # info_logger.info("SUCCESS me")
    return response

