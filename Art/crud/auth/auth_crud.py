from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.auth.token_model import TokenModel
from models.users import UserModel


async def create_user(db: AsyncSession, new_user: UserModel):
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


async def create_token(db: AsyncSession, new_token: TokenModel):
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)


async def delete_token(db: AsyncSession, access_token: str):
    result = await db.execute(select(TokenModel).filter(TokenModel.hash == access_token))
    token = result.scalars().first()
    await db.delete(token)
    await db.commit()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    return result.scalars().first()