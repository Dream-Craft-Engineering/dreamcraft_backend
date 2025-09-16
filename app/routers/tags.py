from fastapi import APIRouter, Depends,HTTPException
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


@router.put("/{tag_id}", response_model=schemas.Tag)
def update_a_tag(
    tag_id: int,
    tag_update: schemas.TagCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    updated_tag = crud.update_tag(db, tag_id, tag_update)
    if updated_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag

@router.delete("/{tag_id}", response_model=schemas.Tag)
def delete_a_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    deleted_tag = crud.delete_tag(db, tag_id)
    if deleted_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return deleted_tag