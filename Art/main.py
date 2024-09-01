from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware

from config.database import engine, Base

from routes.articles import article_routes
from routes.users import users_routes
from routes.auth import auth_routes
from routes.admin import admin_routes

from models.articles.comment_model import CommentModel


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# origins = [
#     "http://frontend:3000",
#     "http://localhost:3000",
# ]

app.add_middleware(
    CORSMiddleware,
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