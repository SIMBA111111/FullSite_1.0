from pydantic import BaseModel, ConfigDict


# class Base(BaseModel):
#     class Config:
#         from_attributes = True


class Base(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
