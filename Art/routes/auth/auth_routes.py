from fastapi import APIRouter, Form, Body, Depends, Header
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, Response

from config.log_config import logger
from dependencies import get_db

from models.users.user_model import UserModel

from schemas.users.users_schemas import SUserBase
from services.auth.auth_services import get_current_user

from services.users import users_services

from services.auth import auth_services

router = APIRouter()


@router.post(path="/register", response_model=SUserBase)
def register(user_data=Body(SUserBase),
             db: Session = Depends(get_db),
             ):
    logger.info(f" - START register")

    user = users_services.create_user(db, user_data)

    logger.info(f" - {user.username} - SUCCESS register")
    return user


@router.post("/login")
def login(username: str = Body(),
          password: str = Body(),
          db: Session = Depends(get_db),
          ):
    logger.info(f" - START login")

    user = auth_services.get_user_by_username(db, username)
    if auth_services.verify_password(password, user.password):
        token = auth_services.create_access_token(db, {"username": username})
    else:
        return JSONResponse({"Error": "Invalid username or password"}, status_code=401)

    response = JSONResponse({"access_token": token}, status_code=200)
    logger.info(f" - {username} - SUCCESS login")
    return response


@router.delete("/logout", response_model=int)
def logout(db: Session = Depends(get_db),
           current_user: UserModel = Depends(get_current_user),
           access_token: str = Header(...)
           ):
    logger.info(f" - {current_user.username} - START logout")

    auth_services.delete_token(db, access_token)

    logger.info(f" - {current_user.username} - SUCCESS logout")
    return Response(status_code=200)
