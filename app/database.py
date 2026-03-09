from contextlib import contextmanager
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
from app.models import *
from app.settings import get_settings
from typing import Dict, List


engine = create_engine(get_settings().database_uri, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_all():
    SQLModel.metadata.drop_all(bind=engine)

def _session_generator():
    with Session(engine) as session:
        yield session

def get_session():
    yield from _session_generator()

@contextmanager
def get_cli_session():
    yield from _session_generator()


SessionDep = Annotated[Session, Depends(get_session)]


# database.py

# Mock database storing todos per user
fake_todos_db: Dict[int, List[dict]] = {
    1: [{"id": 1, "title": "Buy groceries", "completed": False},
        {"id": 2, "title": "Read a book", "completed": True}],
    2: [{"id": 3, "title": "Walk the dog", "completed": False}]
}

# Simple function to get todos by user_id
def get_todos(user_id: int):
    return fake_todos_db.get(user_id, [])

def add_todo(user_id: int, title: str):
    todos = fake_todos_db.setdefault(user_id, [])
    new_id = max([todo["id"] for todo in todos], default=0) + 1
    todo = {"id": new_id, "title": title, "completed": False}
    todos.append(todo)
    return todo

def toggle_todo(user_id: int, todo_id: int):
    todos = fake_todos_db.get(user_id, [])
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            return todo
    return None