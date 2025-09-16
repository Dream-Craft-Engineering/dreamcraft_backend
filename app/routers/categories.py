from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..deps import get_db, get_current_admin

router = APIRouter(prefix="/categories", tags=["Blog Categories"])

@router.post("/", response_model=schemas.Category, status_code=201)
def create_new_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), admin: models.User = Depends(get_current_admin)):
    return crud.create_category(db=db, category=category)

@router.get("/", response_model=List[schemas.Category])
def read_all_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db=db)

@router.put("/{category_id}", response_model=schemas.Category)
def update_a_category(
    category_id: int,
    category_update: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    updated_category = crud.update_category(db, category_id, category_update)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_a_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    deleted_category = crud.delete_category(db, category_id)
    if deleted_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted_category