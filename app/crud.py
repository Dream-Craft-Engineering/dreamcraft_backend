# backend/app/crud.py
from sqlalchemy.orm import Session,joinedload 
from . import models, schemas
from .auth import hash_password

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        phone_number=user.phone_number,
        hashed_password=hashed_pw,
        role_id=user.role_id # Add role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    if 'password' in update_data:
        update_data['hashed_password'] = hash_password(update_data.pop('password'))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_update: schemas.RoleUpdate):
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    update_data = role_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    db_role = get_role(db, role_id)
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role


def create_blog(db: Session, blog: schemas.BlogCreate, author_id: int):
    db_blog = models.Blog(**blog.dict(), author_id=author_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).options(joinedload(models.Blog.author)).filter(models.Blog.id == blog_id).first()

def get_blog_by_slug(db: Session, slug: str):
    return db.query(models.Blog).options(joinedload(models.Blog.author)).filter(models.Blog.slug == slug).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).options(joinedload(models.Blog.author)).offset(skip).limit(limit).all()

def update_blog(db: Session, blog_id: int, blog_update: schemas.BlogUpdate):
    db_blog = get_blog(db, blog_id)
    if not db_blog:
        return None
    update_data = blog_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_blog, key, value)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog