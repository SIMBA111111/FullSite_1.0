from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine, Base

from routes.articles import article_routes
from routes.users import users_routes
from routes.auth import auth_routes
from routes.admin import admin_routes
from routes.options import options_routes

from models.articles.comment_model import CommentModel
from models.options.code_model import CodeModel


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "http://frontend:3000",
    "http://frontend",
    "http://45.91.238.104",
    "https://45.91.238.104",
    "https://24articles.ru",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_routes.router,
                   prefix="/api/v1/articles",
                   tags=["articles"],
                   )

app.include_router(users_routes.router,
                   prefix="/api/v1/users",
                   tags=["users"],
                   )

app.include_router(auth_routes.router,
                   prefix="/api/v1/auth",
                   tags=["auth"],
                   )


app.include_router(admin_routes.router,
                   prefix="/api/v1/admin",
                   tags=["admin"],
                   )

app.include_router(options_routes.router,
                   prefix="/api/v1/options",
                   tags=["options"],
                   )
