from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str
    task_id: int


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    task_id: int
    author_id: int