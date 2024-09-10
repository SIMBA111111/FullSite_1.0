from fastapi.security import OAuth2PasswordBearer

from config.database import async_session


async def get_db():
    async with async_session() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
