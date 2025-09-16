# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List 

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

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        from_attributes = True

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
    author: UserBase
    category: Optional[Category] = None
    tags: List[Tag] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class DashboardStats(BaseModel):
    total_users: int
    published_blogs: int
    draft_blogs: int
    total_categories: int
    total_tags: int