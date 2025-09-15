# backend/app/routers/roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..deps import get_db, get_current_user, get_current_admin

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    return crud.create_role(db=db, role=role)

@router.get("/", response_model=list[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_role = crud.get_role(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    updated_role = crud.update_role(db, role_id, role_update)
    if updated_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

@router.delete("/{role_id}", response_model=schemas.Role)
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin)):
    deleted_role = crud.delete_role(db, role_id)
    if deleted_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted_role