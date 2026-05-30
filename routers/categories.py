from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=schemas.categoryResponse)
def create_category(category: schemas.categoryCreate, db: Session = Depends(get_db)):
    try:
        db_category= models.Category(
            name=category.name
        )

        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="이미 존재하는 카테고리 이름입니다.")

@router.get("", response_model=schemas.categoryList)
def get_category(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return {"items": categories}    

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return db_category