import random

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.options.code_model import CodeModel
from models.users import UserModel


async def user_exist(db: AsyncSession, email: str):
    result = await db.execute(
        select(UserModel)
        .filter(
                UserModel.email == email,
        ).exists().select()
    )
    return result.scalar()


async def create_code(db: AsyncSession, email: str):
    code_obj = CodeModel(code=random.randint(1, 99999999), email=email)
    db.add(code_obj)
    await db.commit()
    await db.refresh(code_obj)
    return code_obj


async def delete_code(db: AsyncSession, code_obj: CodeModel):
    await db.delete(code_obj)
    await db.commit()


async def check_code_exists(db: AsyncSession, email: str, code: int):
    result = await db.execute(
        select(CodeModel)
        .filter(
            CodeModel.code == int(code),
            CodeModel.email == email
        ).exists().select()
    )
    return result.scalar()


async def change_password(db: AsyncSession, new_hashed_password: str, email: str):
    await db.execute(
        update(UserModel)
        .where(UserModel.email == email)
        .values(password=new_hashed_password)
    )
    await db.commit()
