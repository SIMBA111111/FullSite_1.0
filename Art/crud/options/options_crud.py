import random

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.options.code_model import CodeModel
from models.users import UserModel


async def user_is_email(db: AsyncSession, username: str, email: str):
    result = await db.execute(
        select(UserModel)
        .filter(
            and_(
                UserModel.username == username,
                UserModel.email == email,
            )
        )
    )
    return result.scalars().first()


async def create_code(db: AsyncSession, username: str, email: str):
    code_obj = CodeModel(code=random.randint(1, 99999999), username=username, email=email)
    db.add(code_obj)
    await db.commit()
    await db.refresh(code_obj)
    return code_obj


async def delete_code(db: AsyncSession, code_obj: CodeModel):
    await db.delete(code_obj)
    await db.commit()


async def check_code_exists(db: AsyncSession, username: str, email: str, code: str):
    stmt = select(CodeModel).filter(
        and_(
            CodeModel.code == code,
            # CodeModel.email == email,
            # CodeModel.username == username
        )
    ).exists().select()

    result = await db.execute(stmt)
    return result.scalar()
    # print(username)
    # print(email)
    # print(code)
    # result = await db.execute(
    #     select(CodeModel)
    #     .filter(
    #         and_(
    #             CodeModel.code == code,
    #             # CodeModel.email == email,
    #             # CodeModel.username == username,
    #         )
    #     )
    # )
    # return result.scalars().all()


async def change_password(db: AsyncSession, new_hashed_password: str, email: str):
    await db.execute(
        update(UserModel)
        .where(UserModel.email == email)
        .values(password=new_hashed_password)
    )
    await db.commit()
