from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..deps import get_db, get_current_user, get_current_admin

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=schemas.Role, status_code=201)
def create_new_role(
    role: schemas.RoleCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_admin)
):
    return crud.create_role(db=db, role=role)

@router.get("/", response_model=List[schemas.Role])
def read_all_roles(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles

@router.put("/{role_id}", response_model=schemas.Role)
def update_existing_role(
    role_id: int, 
    role_update: schemas.RoleUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_admin)
):
    updated_role = crud.update_role(db, role_id, role_update)
    if updated_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

@router.delete("/{role_id}", response_model=schemas.Role)
def delete_existing_role(
    role_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_admin)
):
    deleted_role = crud.delete_role(db, role_id)
    if deleted_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted_role