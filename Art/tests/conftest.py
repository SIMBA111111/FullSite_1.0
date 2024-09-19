import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config.database import Base
from main import app
from dependencies import get_db
from services.auth.auth_services import get_current_user

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs

from models.users import UserModel
from models.users.user_model import AnonymousUser

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./TestBD.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_test_db():
    async with TestingSessionLocal() as session:
        yield session

client = TestClient(app)
