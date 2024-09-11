from fastapi import Depends, Body, Header
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from config.log_config import info_logger

from models.users.user_model import UserModel, AnonymousUser

from schemas.admin.admin_schemas import BidListResponseModel, FileDownloadRequest
from schemas.articles.articles_schemas import SSlug

from services.auth.auth_services import get_current_user
from services.admin import admin_services


router = APIRouter()


@router.get("/bid-list", response_model=list[BidListResponseModel])
async def get_bid_list(db: AsyncSession = Depends(get_db),
                       current_user: UserModel = Depends(get_current_user),
                       ):
    await admin_services.check_is_admin_user(current_user)
    info_logger.info(f" - {current_user.username} - START get bid list")

    bid_list_response = await admin_services.get_bid_list(db)

    response = JSONResponse(status_code=200, content=[item.dict() for item in bid_list_response])
    info_logger.info(f" - {current_user.username} - SUCCESS get bid list")
    return response


@router.post("/download-file")
async def download_file(filename: FileDownloadRequest = Body(),
                        current_user: UserModel = Depends(get_current_user),
                        ):
    await admin_services.check_is_admin_user(current_user)
    info_logger.info(f" - {current_user.username} - START download file")

    path = await admin_services.path_to_file(filename)

    response = FileResponse(path, filename=filename.filename, status_code=200)
    info_logger.info(f" - {current_user.username} - SUCCESS download file")
    return response


@router.post("/approve-bid")
async def approve_bid(filename: FileDownloadRequest = Body(),
                      db: AsyncSession = Depends(get_db),
                      current_user: UserModel = Depends(get_current_user),
                      ):
    await admin_services.check_is_admin_user(current_user)
    info_logger.info(f" - {current_user.username} - START approve bid")

    html_file_name = await admin_services.create_html_file(filename)
    await admin_services.create_paths_in_src_in_html_files(filename, html_file_name)
    await admin_services.process_html_file(html_file_name, html_file_name)
    await admin_services.approve_article_bid_approved(filename, db)

    response = JSONResponse(status_code=200, content={"Success": "The article has been approved"})
    info_logger.info(f" - {current_user.username} - SUCCESS approve bid")
    return response


@router.post("/cancel-bid")
async def cancel_bid(filename: FileDownloadRequest = Body(),
                     db: AsyncSession = Depends(get_db),
                     current_user: UserModel | AnonymousUser = Depends(get_current_user),
                     ):
    await admin_services.check_is_admin_user(current_user)
    info_logger.info(f" - {current_user.username} - START cancel bid")

    await admin_services.cancel_bid(db, filename)

    response = JSONResponse(status_code=200, content={"Success": "The article has been canceled"})
    info_logger.info(f" - {current_user.username} - SUCCESS cancel bid")
    return response


@router.post("/disable-article")
async def disable_article(db: AsyncSession = Depends(get_db),
                          current_user: UserModel | AnonymousUser = Depends(get_current_user),
                          disable: bool = Body(),
                          slug: SSlug = Body(),
                          ):

    await admin_services.check_is_admin_user(current_user)
    info_logger.info(f" - {current_user.username} - START disable article")

    await admin_services.disable_article(db, disable, slug)

    response = JSONResponse(status_code=200, content={"Success": "The article has been disabled"})
    info_logger.info(f" - {current_user.username} - SUCCESS disable article")
    return response


@router.get("/get-all-articles")
async def get_all_articles(db: AsyncSession = Depends(get_db),
                           current_user: UserModel | AnonymousUser = Depends(get_current_user),
                           page: int = 1
                           ):
    await admin_services.check_is_admin_user(current_user)
    info_logger.info(f" - {current_user.username} - START get all articles admin")

    articles = await admin_services.get_all_articles(db, page)

    # response = JSONResponse(status_code=200, content=articles)
    info_logger.info(f" - {current_user.username} - SUCCESS get all articles admin")
    # return response
    return articles
