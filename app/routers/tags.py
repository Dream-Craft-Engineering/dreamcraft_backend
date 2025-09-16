from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..deps import get_db, get_current_admin

router = APIRouter(prefix="/tags", tags=["Blog Tags"])

@router.post("/", response_model=schemas.Tag, status_code=201)
def create_new_tag(tag: schemas.TagCreate, db: Session = Depends(get_db), admin: models.User = Depends(get_current_admin)):
    return crud.create_tag(db=db, tag=tag)

@router.get("/", response_model=List[schemas.Tag])
def read_all_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db=db)