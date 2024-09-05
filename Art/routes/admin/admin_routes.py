from fastapi import Depends, Body, Header
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse, Response
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from dependencies import get_db
from config.log_config import logger

from models.users.user_model import UserModel, AnonymousUser

from schemas.admin.admin_schemas import BidListResponseModel, FileDownloadRequest

from services.auth.auth_services import get_current_user
from services.admin import admin_services


router = APIRouter()


@router.get("/bid-list", response_model=list[BidListResponseModel])
def get_bid_list(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    user_agent: str = Header(),
):
    print(current_user)
    admin_services.check_is_admin_user(current_user)
    logger.info(f" - {current_user.username} - START get_bid_list - {user_agent}")

    bid_list_response = admin_services.get_bid_list(db)

    response = JSONResponse(status_code=200, content=[item.dict() for item in bid_list_response])
    logger.info(f" - {current_user.username} - SUCCESS get_bid_list - {user_agent}")
    return response


@router.post("/download-file")
def download_file(filename: FileDownloadRequest = Body(),
                  current_user: UserModel = Depends(get_current_user),
                  user_agent: str = Header(),
                  ):
    admin_services.check_is_admin_user(current_user)
    logger.info(f" - {current_user.username} - START download_file - {user_agent}")

    path = admin_services.path_to_file(filename)

    response = FileResponse(path, filename=filename.filename, status_code=200)
    logger.info(f" - {current_user.username} - SUCCESS download_file - {user_agent}")
    return response


@router.post("/approve-bid")
def approve_bid(filename: FileDownloadRequest = Body(),
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user),
                user_agent: str = Header(),
                ):
    admin_services.check_is_admin_user(current_user)
    logger.info(f" - {current_user.username} - START approve_bid - {user_agent}")

    html_file_name = admin_services.create_html_file(filename)
    admin_services.create_paths_in_src_in_html_files(filename, html_file_name)
    admin_services.process_html_file(html_file_name, html_file_name)
    admin_services.approve_article_bid_approved(filename, db)

    response = JSONResponse(status_code=200, content={"Success": "Статья одобрена"})
    logger.info(f" - {current_user.username} - SUCCESS approve_bid - {user_agent}")
    return response


@router.post("/cancel-bid")
def cancel_bid(filename: FileDownloadRequest = Body(),
               db: Session = Depends(get_db),
               current_user: UserModel | AnonymousUser = Depends(get_current_user),
               user_agent: str = Header(),
               ):
    print("current_user - ", current_user)
    admin_services.check_is_admin_user(current_user)
    logger.info(f" - {current_user.username} - START cancel bid - {user_agent}")

    # admin_services.cancel_bid(db, filename)

    response = JSONResponse(status_code=200, content={"Success": "Статья отменена"})
    logger.info(f" - {current_user.username} - SUCCESS cancel bid - {user_agent}")
    return response


