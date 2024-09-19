from fastapi import APIRouter, Form, Body, Depends, Header
from fastapi.responses import JSONResponse, Response

from sqlalchemy.ext.asyncio import AsyncSession

from config.log_config import info_logger
from dependencies import get_db

from models.users.user_model import UserModel

from schemas.users.users_schemas import SUserBase

from services.auth.auth_services import get_current_user
from services.users import users_services
from services.auth import auth_services


router = APIRouter()


@router.post(path="/register", response_model=SUserBase)
async def register(user_data=Body(SUserBase),
                   db: AsyncSession = Depends(get_db),
                   ):
    info_logger.info(f" - START register")

    user = await users_services.create_user(db, user_data)

    info_logger.info(f" - {user.username} - SUCCESS register")
    return user


@router.post("/login")
async def login(username: str = Body(),
                password: str = Body(),
                db: AsyncSession = Depends(get_db),
                ):
    info_logger.info(f" - {username} - START login")

    user = await auth_services.get_user_by_username(db, username)
    if await auth_services.verify_password(password, user.password):
        token = await auth_services.create_access_token(db, {"username": username})
    else:
        return JSONResponse({"Error": "Invalid username or password"}, status_code=401)

    response = JSONResponse({"access_token": token}, status_code=200)
    info_logger.info(f" - {username} - SUCCESS login")
    return response


@router.delete("/logout", response_model=int)
async def logout(db: AsyncSession = Depends(get_db),
                 current_user: UserModel = Depends(get_current_user),
                 access_token: str = Header(...),
                 ):
    info_logger.info(f" - {current_user.username} - START logout")

    await auth_services.delete_token(db, access_token)

    info_logger.info(f" - {current_user.username} - SUCCESS logout")
    return Response(status_code=200)