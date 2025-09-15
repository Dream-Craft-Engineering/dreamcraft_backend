# backend/app/routers/blogs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models # <-- Import models
from ..deps import get_db, get_current_user # <-- Import get_current_user

router = APIRouter(prefix="/blogs", tags=["blogs"])

# --- THIS IS THE NEW, UNCOMMENTED ENDPOINT ---
@router.post("/", response_model=schemas.Blog, status_code=201)
def create_new_blog(
    blog: schemas.BlogCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new blog post. The author is the currently logged-in user.
    """
    return crud.create_blog(db=db, blog=blog, author_id=current_user.id)

# --- Public GET endpoints (no changes) ---
@router.get("/", response_model=List[schemas.Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs

@router.get("/{slug}", response_model=schemas.Blog)
def read_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_slug(db, slug=slug)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog


# --- ADD THESE TWO ENDPOINTS ---
@router.put("/{blog_id}", response_model=schemas.Blog)
def update_blog_item(
    blog_id: int,
    blog_update: schemas.BlogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    # Optional: Check if the current user is the author
    if db_blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog")
    return crud.update_blog(db=db, blog_id=blog_id, blog_update=blog_update)

@router.delete("/{blog_id}", response_model=schemas.Blog)
def delete_blog_item(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this blog")
    return crud.delete_blog(db=db, blog_id=blog_id)