from datetime import timedelta, datetime, timezone

import jwt
import os

from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from config.log_config import error_logger
from models.auth.token_model import TokenModel
from models.users import UserModel
from models.users.user_model import AnonymousUser

from crud.auth import auth_crud

from dependencies import get_db

from fastapi import status, Depends, HTTPException, Body, Header

from jose import jwt

from typing import Union, Any


# SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
REFRESH_SECRET_KEY = "09d25e094faa6ca2556c818166b7a6563b93f7599f6f0f4gta6cf33b00e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(db: AsyncSession, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    new_token = TokenModel(hash=encoded_jwt, expiration=expire)
    try:
        await auth_crud.create_token(db, new_token)
    except Exception as e:
        error_logger.error(f"Failed to create a new token. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Failed to create a new token. Error: {e}"})
    return encoded_jwt


async def is_hashed_password(password: str) -> str:
    return await run_in_threadpool(lambda: pwd_context.hash(password))


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await run_in_threadpool(lambda: pwd_context.verify(plain_password, hashed_password))


# async def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.now() + expires_delta
#     else:
#         expires_delta = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
#     return encoded_jwt
#
#
# async def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.now() + expires_delta
#     else:
#         expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
#
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
#     return encoded_jwt


async def get_user_by_username(db: AsyncSession, username: str):
    try:
        current_user = await auth_crud.get_user_by_username(db, username)
    except Exception as e:
        error_logger.error(f"Couldn't get a user by username. Error: {e}")
        raise HTTPException(status_code=400,
                            detail={"Error": f"Couldn't get a user by username. Error: {e}"}
                            )
    return current_user


async def get_current_user(Authorization: str = Header(default=None),
                           db: AsyncSession = Depends(get_db),
                           ):
    if Authorization is None:
        result = await db.execute(select(AnonymousUser).filter(AnonymousUser.username == "AnonymousUser"))
        return result.scalars().first()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    # finally:
    #     print("!!!")
    #     token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def delete_token(db: AsyncSession, access_token: str):
    try:
        await auth_crud.delete_token(db, access_token)
    except Exception as e:
        error_logger.error(f"The token could not be deleted. Error: {e}")
        raise HTTPException(status_code=400, detail={"message": f"The token could not be deleted. Error: {e}"})
    return 200


async def is_authed(current_user: UserModel | AnonymousUser):
    if isinstance(current_user, AnonymousUser):
        raise HTTPException(status_code=403, detail={"Error": "You need to login"})
