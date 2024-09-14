from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from models.base_model import BaseModel


class CodeModel(BaseModel):
    __tablename__ = "code"

    code: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)
