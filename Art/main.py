from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine, Base

from routes.articles import article_routes
from routes.users import users_routes
from routes.auth import auth_routes
from routes.admin import admin_routes
from routes.options import options_routes

from contextlib import asynccontextmanager

from models.articles.comment_model import CommentModel


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
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # You can specify domains here, e.g., ["http://localhost:3000"]
    allow_origins=["*"],  # You can specify domains here, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, e.g., GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
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