from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from config.log_config import logger
from dependencies import get_db
from schemas.users.users_schemas import SUsername
from services.users import users_services

router = APIRouter()


@router.get("/get-all-authors")
def get_all_authors(db: Session = Depends(get_db)):
    logger.info(f" - START get_all_author")

    users_ordered_by_article_count = users_services.get_all_authors(db)

    logger.info(f" - SUCCESS get_all_authors")
    return users_ordered_by_article_count


@router.post("/get-author")
def get_author(db: Session = Depends(get_db),
               username: SUsername = Body()
               ):
    logger.info("START get_author")

    author = users_services.get_author(db, username)

    response = JSONResponse(status_code=200, content={"author": author})
    logger.info("SUCCESS get_author")
    return response
