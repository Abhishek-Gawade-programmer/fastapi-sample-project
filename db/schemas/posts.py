from pydantic import BaseModel, Field


class PostBase(BaseModel):
    text: str = Field(..., description="post content")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
