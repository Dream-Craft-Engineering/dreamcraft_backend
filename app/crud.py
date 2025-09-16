from sqlalchemy.orm import Session, joinedload
from . import models, schemas
from .auth import hash_password



def get_user(db: Session, user_id: int):
    # Eagerly load the user's role to prevent extra database queries
    return db.query(models.User).options(joinedload(models.User.role)).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).options(joinedload(models.User.role)).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload(models.User.role)).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        phone_number=user.phone_number,
        hashed_password=hashed_pw,
        role_id=user.role_id
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

def delete_role(db: Session, role_id: int):
    db_role = get_role(db, role_id)
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role


def get_category(db: Session, category_id: int):
    return db.query(models.BlogCategory).filter(models.BlogCategory.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BlogCategory).offset(skip).limit(limit).all()

# --- THIS FUNCTION IS NOW FIXED ---
def create_category(db: Session, category: schemas.CategoryCreate):
    # Using **category.dict() unpacks all fields from the form (name and description)
    db_category = models.BlogCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category



def get_tag(db: Session, tag_id: int):
    return db.query(models.BlogTag).filter(models.BlogTag.id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BlogTag).offset(skip).limit(limit).all()

# --- THIS FUNCTION IS NOW FIXED ---
def create_tag(db: Session, tag: schemas.TagCreate):
    # Using **tag.dict() unpacks all fields from the form
    db_tag = models.BlogTag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag



def create_blog(db: Session, blog: schemas.BlogCreate, author_id: int):
    # Separate the tag_ids from the rest of the blog data
    tag_ids = blog.tag_ids
    blog_data = blog.dict(exclude={'tag_ids'})
    
    
    db_blog = models.Blog(**blog_data, author_id=author_id)
    
    
    if tag_ids:
        tags = db.query(models.BlogTag).filter(models.BlogTag.id.in_(tag_ids)).all()
        db_blog.tags = tags  # Assign the list of Tag objects
        
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int):

    return db.query(models.Blog).options(
        joinedload(models.Blog.author),
        joinedload(models.Blog.category),
        joinedload(models.Blog.tags)
    ).filter(models.Blog.id == blog_id).first()


def get_blog_by_slug(db: Session, slug: str):
    return db.query(models.Blog).options(
        joinedload(models.Blog.author),
        joinedload(models.Blog.category),
        joinedload(models.Blog.tags)
    ).filter(models.Blog.slug == slug).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    
    return db.query(models.Blog).options(
        joinedload(models.Blog.author),
        joinedload(models.Blog.category),
        joinedload(models.Blog.tags)
    ).filter(models.Blog.status == 'published').offset(skip).limit(limit).all()


def get_blogs_by_author(db: Session, author_id: int):
 
    return db.query(models.Blog).options(
        joinedload(models.Blog.category),
        joinedload(models.Blog.tags)
    ).filter(models.Blog.author_id == author_id).order_by(models.Blog.id.desc()).all()

def update_blog(db: Session, blog_id: int, blog_update: schemas.BlogUpdate):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not db_blog:
        return None

    update_data = blog_update.dict(exclude_unset=True)
    

    if 'tag_ids' in update_data:
        tag_ids = update_data.pop('tag_ids')
        if tag_ids is not None:
            tags = db.query(models.BlogTag).filter(models.BlogTag.id.in_(tag_ids)).all()
            db_blog.tags = tags

    # Update remaining fields
    for key, value in update_data.items():
        setattr(db_blog, key, value)
        
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog

def get_dashboard_stats(db: Session):
    total_users = db.query(models.User).count()
    published_blogs = db.query(models.Blog).filter(models.Blog.status == 'published').count()
    draft_blogs = db.query(models.Blog).filter(models.Blog.status == 'draft').count()
    total_categories = db.query(models.BlogCategory).count()
    total_tags = db.query(models.BlogTag).count()
    return schemas.DashboardStats(
        total_users=total_users,
        published_blogs=published_blogs,
        draft_blogs=draft_blogs,
        total_categories=total_categories,
        total_tags=total_tags
    )

def update_category(db: Session, category_id: int, category_update: schemas.CategoryCreate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    update_data = category_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# === UPDATE Blog Tag CRUD Functions ===
def update_tag(db: Session, tag_id: int, tag_update: schemas.TagCreate):
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    update_data = tag_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db_tag = get_tag(db, tag_id)
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag