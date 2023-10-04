from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    description: str
    is_done: bool = False
    user_id: int
