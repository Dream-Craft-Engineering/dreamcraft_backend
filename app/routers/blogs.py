# backend/app/routers/blogs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Blog, BlogCreate, BlogUpdate
from ..crud import create_blog, get_blog, get_blogs, update_blog, delete_blog
from ..deps import get_db, get_current_user
from ..models import User, Blog as BlogModel  # Added for type hint

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.post("/", response_model=Blog)
def create_blog_item(blog: BlogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_blog(db, blog, current_user.id)

@router.get("/", response_model=list[Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_blogs(db, skip=skip, limit=limit)

@router.get("/{blog_id}", response_model=Blog)
def read_blog(blog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = get_blog(db, blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

@router.put("/{blog_id}", response_model=Blog)
def update_blog_item(blog_id: int, blog_update: BlogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = get_blog(db, blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_blog = update_blog(db, blog_id, blog_update)
    return updated_blog

@router.delete("/{blog_id}", response_model=Blog)
def delete_blog_item(blog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = get_blog(db, blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted_blog = delete_blog(db, blog_id)
    return deleted_blog