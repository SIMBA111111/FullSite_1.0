from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from config.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[str] = mapped_column(default=func.now())
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    )

    # @declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return f"{cls.__name__.lower()}s"
