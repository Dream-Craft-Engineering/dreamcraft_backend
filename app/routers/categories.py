from fastapi import APIRouter, Depends
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