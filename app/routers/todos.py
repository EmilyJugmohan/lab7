from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.schemas.todos import Todo, TodoCreate
from app.database import SessionDep
from app.models.todo import Todo as TodoModel
from app.auth import AuthDep

router = APIRouter(tags=["Todos"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/todos", response_model=List[Todo])
def get_todos(db: SessionDep, user: AuthDep = Depends()):
    return db.exec(select(TodoModel).where(TodoModel.user_id == user.id)).all()


@router.post("/todos", response_model=Todo)
def add_todo(todo: TodoCreate, db: SessionDep, user: AuthDep = Depends()):
    new_todo = TodoModel(title=todo.title, completed=False, user_id=user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


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


@router.get("/todos/ui")
def todos_ui(request: Request, db: SessionDep, user: AuthDep = Depends()):
    todos = db.exec(select(TodoModel).where(TodoModel.user_id == user.id)).all()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos})



#writing so i can test the commit and push functionality of git, ignore this code

#another test