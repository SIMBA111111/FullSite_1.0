from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from config.database import SessionLocal

from models.users.user_model import UserModel


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
