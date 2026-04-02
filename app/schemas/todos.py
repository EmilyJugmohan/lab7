from typing import Optional
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int


class TodoCreate(BaseModel):
    title: str