# backend/app/schemas.py
from pydantic import BaseModel, EmailStr

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: str | None = None

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True  # For ORM mode

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_id: int

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    role_id: int | None = None
    is_active: bool | None = None

class User(UserBase):
    id: int
    is_active: bool
    role: Role

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class Blog(BlogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True