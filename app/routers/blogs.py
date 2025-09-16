from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..deps import get_db, get_current_user, get_current_admin

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/", response_model=schemas.Blog, status_code=201)
def create_new_blog(
    blog: schemas.BlogCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_admin)
):
    return crud.create_blog(db=db, blog=blog, author_id=current_user.id)

@router.get("/", response_model=List[schemas.Blog])
def read_published_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs


@router.get("/my-blogs", response_model=List[schemas.Blog])
def read_my_blogs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_blogs_by_author(db=db, author_id=current_user.id)


@router.get("/dashboard-blogs", response_model=List[schemas.Blog])
def read_blogs_for_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Now accessible by any user
):

    return crud.get_all_blogs_for_dashboard(db=db)

@router.get("/{blog_id}", response_model=schemas.Blog)
def read_blog_by_id(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) 
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog


@router.get("/by-id/{blog_id}", response_model=schemas.Blog)
def read_blog_by_id(
    blog_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Fetch a single blog post by its unique integer ID.
    Used for the admin edit page.
    """
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

@router.get("/{slug}", response_model=schemas.Blog)
def read_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_slug(db, slug=slug)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog


@router.put("/{blog_id}", response_model=schemas.Blog)
def update_blog_post(
    blog_id: int,
    blog_update: schemas.BlogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if db_blog.author_id != current_user.id and current_user.role.name.lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    return crud.update_blog(db=db, blog_id=blog_id, blog_update=blog_update)


@router.delete("/{blog_id}", response_model=schemas.Blog)
def delete_blog_post(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if db_blog.author_id != current_user.id and current_user.role.name.lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    return crud.delete_blog(db=db, blog_id=blog_id)