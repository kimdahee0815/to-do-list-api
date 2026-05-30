from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from fastapi import APIRouter, Depends, HTTPException, Query, status

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("", response_model=schemas.todoResponse)
def create_todo(todo: schemas.todoCreate, db: Session = Depends(get_db)):
    db_todo= models.Todo(
        title=todo.title,
        description=todo.description,
        is_done=todo.is_done,
        priority=todo.priority
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
    

@router.get("/{todo_id}", response_model=schemas.todoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    return db_todo

@router.get("", response_model=schemas.todoList)
def get_todolist(is_done: Optional[bool] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(models.Todo)
    if is_done is not None:
        query = query.filter(models.Todo.is_done == is_done)

    return {"items": query.all()}

@router.patch("/{todo_id}", response_model=schemas.todoResponse)
def update_todo(todo_id: int, todo_data: schemas.todoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if todo_data.title is not None:
        db_todo.title = todo_data.title
    if todo_data.description is not None:
        db_todo.description = todo_data.description
    if todo_data.is_done is not None:
        db_todo.is_done = todo_data.is_done
    if todo_data.priority is not None:
        db_todo.priority = todo_data.priority

    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return db_todo