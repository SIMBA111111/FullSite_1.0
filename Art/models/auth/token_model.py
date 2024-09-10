from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class TokenModel(BaseModel):

    __tablename__ = 'Token'

    hash: Mapped[str] = mapped_column(String, unique=True)
    expiration: Mapped[str] = mapped_column(DateTime)
