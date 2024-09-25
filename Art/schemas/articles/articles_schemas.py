from ..base_schemas import Base, BaseModel
from ..users.users_schemas import SAuthorsList


class SSlug(Base):
    slug: str


class SArticleListWithAuthors(BaseModel):
    name: str
    intro_text: str
    slug: str
    count_views: int
    title: str
    date: str
    user: SAuthorsList
