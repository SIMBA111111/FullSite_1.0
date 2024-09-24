from ..base_schemas import BaseModel


class SUserBase(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str
    username: str


class SUsername(BaseModel):
    username: str


class SAuthorsList(BaseModel):
    first_name: str
    last_name: str
    email: str | None = None
    username: str
    views_count: int | None = None
    first_article_date: str | None = None

