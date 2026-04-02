from typing import Optional
from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False

    user_id: int = Field(foreign_key="user.id", index=True)