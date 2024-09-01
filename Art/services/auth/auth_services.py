from datetime import timedelta, datetime, timezone

import jwt
from jwt.exceptions import PyJWTError
from sqlalchemy.orm import Session

from config.log_config import logger
from models.auth.token_model import TokenModel
from models.users.user_model import AnonymousUser

from crud.users.users_crud import pwd_context
from crud.auth import auth_crud

from dependencies import get_db

from fastapi import status, Depends, HTTPException, Body, Header


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(db: Session, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    new_token = TokenModel(hash=encoded_jwt, expiration=expire)
    try:
        auth_crud.create_token(db, new_token)
    except Exception as e:
        logger.error(f"Failed to create a new token. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Failed to create a new token. Error: {e}"})
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str):
    try:
        current_user = auth_crud.get_user_by_username(db, username)
    except Exception as e:
        logger.error(f"Couldn't get a user by username. Error: {e}")
        raise HTTPException(status_code=400,
                            detail={"Error": f"Couldn't get a user by username. Error: {e}"}
                            )
    return current_user


# Декодирование токена и проверка пользователя
def get_current_user(Authorization: str = Header(default=None),
                     db: Session = Depends(get_db)
                     ):
    if Authorization is None:
        return db.query(AnonymousUser).filter(AnonymousUser.username == "AnonymousUser").first()

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
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def delete_token(db: Session, access_token: str):
    try:
        auth_crud.delete_token(db, access_token)
    except Exception as e:
        logger.error(f"The token could not be deleted. Error: {e}")
        raise HTTPException(status_code=400, detail={"message": f"The token could not be deleted. Error: {e}"})
    return 200
