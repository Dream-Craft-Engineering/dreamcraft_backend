# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List # <--- THIS IS THE FIX

# --- Role Schemas ---
class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None

class Role(RoleBase):
    id: int
    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone_number: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    role: Role
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str
    role_id: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None

# --- NEW Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- NEW Tag Schemas ---
class TagBase(BaseModel):
    name: str
    description: Optional[str] = None

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        from_attributes = True

# --- UPDATED Blog Schemas ---
class BlogBase(BaseModel):
    title: str
    slug: str
    content: str
    image_url: Optional[str] = None
    status: str = 'draft'

class BlogCreate(BlogBase):
    category_id: int
    tag_ids: List[int] = []

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class Blog(BlogBase):
    id: int
    author_id: int
    author: "UserBase" 
    category: Optional[Category] = None
    tags: List[Tag] = []

    class Config:
        from_attributes = True
        
# --- Dashboard Schema ---
class DashboardStats(BaseModel):
    total_users: int
    published_blogs: int
    draft_blogs: int
    total_categories: int
    total_tags: int

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str

# Forward reference resolution
Blog.model_rebuild()

class ProjectImageBase(BaseModel):
    url: str

class ProjectImageCreate(ProjectImageBase):
    pass

class ProjectImage(ProjectImageBase):
    id: int
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str
    category: str
    location: str
    image_url: str
    client: str
    completion_date: str
    value: str
    description: str

class ProjectCreate(ProjectBase):

    gallery_urls: List[str] = []

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    client: Optional[str] = None
    completion_date: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    gallery_urls: Optional[List[str]] = None

class Project(ProjectBase):
    id: int
    images: List[ProjectImage] = [] 

    class Config:
        from_attributes = True