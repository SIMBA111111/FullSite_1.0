import pytest
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from main import app

from dependencies import get_db
from models.users import UserModel
from models.users.user_model import AnonymousUser
from services.auth.auth_services import get_current_user
from tests.conftest import get_test_db, init_db, drop_db


@pytest.fixture(scope="function")
async def application():
    app.dependency_overrides[get_db] = get_test_db
    await init_db()
    yield
    await drop_db()


@pytest.fixture(scope="function")
async def data_test_db(db: AsyncSession = Depends(get_test_db)):
    anonymous_user = AnonymousUser(username="AnonymousUser")
    admin_user = UserModel(username="admin",
                           password="admin",
                           first_name="admin",
                           last_name="admin",
                           is_admin_user=True
                           )

    db.add(anonymous_user)
    db.add(admin_user)
    await db.refresh(anonymous_user)
    await db.refresh(admin_user)
    await db.commit()


@pytest.fixture
async def override_get_current_user_for_admin():
    async def mock_get_current_user():
        return UserModel(username="admin", is_admin_user=True)

    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides[get_current_user] = get_current_user
