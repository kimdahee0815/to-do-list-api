from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from fastapi import APIRouter, Depends, HTTPException, Query, status

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("", response_model=schemas.todoResponse)
def create_todo(todo: schemas.todoCreate, db: Session = Depends(get_db)):

    if todo.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == todo.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db_todo= models.Todo(
        title=todo.title,
        description=todo.description,
        is_done=todo.is_done,
        priority=todo.priority,
        category_id=todo.category_id
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
    
    if db_todo.category is not None:
        print("category name : ", db_todo.category.name)
    

    return db_todo

@router.get("", response_model=schemas.todoList)
def get_todolist(is_done: Optional[bool] = Query(default=None), priority: Optional[int] = Query(default=None), 
                db: Session = Depends(get_db)):
    query = db.query(models.Todo)
    if is_done is not None:
        query = query.filter(models.Todo.is_done == is_done)
    if priority is not None:
        query = query.filter(models.Todo.priority == priority)

    return {"items": query.all()}

@router.patch("/{todo_id}", response_model=schemas.todoResponse)
def update_todo(todo_id: int, todo_data: schemas.todoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if todo_data.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == todo_data.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        
    if todo_data.title is not None:
        db_todo.title = todo_data.title
    if todo_data.description is not None:
        db_todo.description = todo_data.description
    if todo_data.is_done is not None:
        db_todo.is_done = todo_data.is_done
    if todo_data.priority is not None:
        db_todo.priority = todo_data.priority
    if todo_data.category_id is not None:
        db_todo.category_id = todo_data.category_id

    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", response_model=schemas.todoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return db_todo