from sqlalchemy.orm import Session

from models.auth.token_model import TokenModel
from models.users import UserModel


def create_user(db: Session, new_user: UserModel):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def create_token(db: Session, new_token: TokenModel):
    db.add(new_token)
    db.commit()
    db.refresh(new_token)


def delete_token(db: Session, access_token: str):
    token = db.query(TokenModel).filter(TokenModel.hash == access_token).first()
    db.delete(token)
    db.commit()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()