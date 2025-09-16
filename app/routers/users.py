from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..deps import get_db, get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user) 
):
   
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user) 
):
    """
    Retrieve a single user by ID. Accessible by any logged-in user.
    """
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# --- NEW: Endpoint for a user to delete their own account ---
@router.delete("/me", response_model=schemas.User)
def delete_own_account(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Allows a logged-in user to delete their own account.
    """
    deleted_user = crud.delete_user(db, user_id=current_user.id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user_details(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user) # Now depends on any logged-in user
):
    """
    Update a user's details.
    - Admins can update any user.
    - Regular users can only update their own profile.
    """
    is_admin = current_user.role.name.lower() == 'admin'
    
    # Check if the user has permission to perform the update
    if not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
        
    # Prevent non-admins from changing a role_id
    if not is_admin and user_update.role_id is not None and user_update.role_id != current_user.role_id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to change user roles"
        )

    updated_user = crud.update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_another_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_admin) # This remains admin-only
):
    """
    Allows an admin to delete another user.
    """
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Admins cannot delete themselves using this route.")
    
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user