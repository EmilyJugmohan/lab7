from fastapi import APIRouter, Depends, Request
from typing import List
from fastapi.templating import Jinja2Templates

from app.schemas.todo import Todo, TodoCreate  # Pydantic schemas for todos
from app.database import SessionDep
from app.models.todo import Todo as TodoModel  # SQLModel Todo table
from app.auth import AuthDep  # Auth dependency

router = APIRouter(tags=["Todos"])
templates = Jinja2Templates(directory="app/templates")

# Get all todos for the current user
@router.get("/todos", response_model=List[Todo])
def get_todos(db: SessionDep, user: AuthDep = Depends()):
    todos = db.exec(
        select(TodoModel).where(TodoModel.user_id == user.id)
    ).all()
    return todos

# Add new todo
@router.post("/todos", response_model=Todo)
def add_todo(todo: TodoCreate, db: SessionDep, user: AuthDep = Depends()):
    new_todo = TodoModel(title=todo.title, completed=False, user_id=user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# Toggle completed
@router.post("/todos/{todo_id}/toggle", response_model=Todo)
def toggle_todo(todo_id: int, db: SessionDep, user: AuthDep = Depends()):
    todo = db.get(TodoModel, todo_id)
    if not todo or todo.user_id != user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = not todo.completed
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

# UI page
@router.get("/todos/ui")
def todos_ui(request: Request, db: SessionDep, user: AuthDep = Depends()):
    todos = db.exec(
        select(TodoModel).where(TodoModel.user_id == user.id)
    ).all()
    return templates.TemplateResponse(
        "todos.html",
        {"request": request, "todos": todos}
    )