# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone_number: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

# --- Blog Schemas ---
class BlogBase(BaseModel):
    # --- THIS BLOCK IS NOW CORRECTLY INDENTED ---
    slug: str
    title: str
    content: str
    category: Optional[str] = None
    date: Optional[str] = None
    excerpt: Optional[str] = None
    is_featured: Optional[bool] = False
    image_url: Optional[str] = None
    image_url_2: Optional[str] = None
    image_url_3: Optional[str] = None
    # ---------------------------------------------

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    excerpt: Optional[str] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None
    image_url_2: Optional[str] = None
    image_url_3: Optional[str] = None

class Blog(BlogBase):
    id: int
    author_id: int
    author: UserBase 

    class Config:
        from_attributes = True

# --- Other Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None