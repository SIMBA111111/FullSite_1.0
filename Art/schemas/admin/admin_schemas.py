from pydantic import ConfigDict

from ..base_schemas import BaseModel, Base


class FileDownloadRequest(Base):
    filename: str


class BidListResponseModel(BaseModel):
    name: str
    bid_approved: bool
    intro_text: str

    model_config = ConfigDict(
        arbitrary_types_allowed = True
    )




