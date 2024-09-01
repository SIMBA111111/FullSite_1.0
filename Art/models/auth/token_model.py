import datetime
from typing import List, Optional
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base_model import BaseModel


class TokenModel(BaseModel):

    __tablename__ = 'Token'

    hash: Mapped[str] = mapped_column(String, unique=True)
    expiration: Mapped[str] = mapped_column(DateTime)
