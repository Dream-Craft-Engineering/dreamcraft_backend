from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from .database import Base

blog_tag_association = Table(
    'blog_tag_association', Base.metadata,
    Column('blog_id', Integer, ForeignKey('blogs.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('blog_tags.id'), primary_key=True)
)


class BlogCategory(Base):
    __tablename__ = "blog_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True) 
    blogs = relationship("Blog", back_populates="category")

class BlogTag(Base):
    __tablename__ = "blog_tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True) 
    blogs = relationship("Blog", secondary=blog_tag_association, back_populates="tags")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(191), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")
    blogs = relationship("Blog", back_populates="author")


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(191), nullable=False)
    slug = Column(String(191), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(191)) 
    
    status = Column(Enum('draft', 'published', name='blogstatusenum'), default='draft', nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")

    category_id = Column(Integer, ForeignKey("blog_categories.id"))
    category = relationship("BlogCategory", back_populates="blogs")
    
    
    tags = relationship("BlogTag", secondary=blog_tag_association, back_populates="blogs")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(191), nullable=False)
    category = Column(String(100), nullable=False) 
    location = Column(String(191), nullable=False)
    image_url = Column(String(191)) 
    
    client = Column(String(191))
    completion_date = Column(String(100)) 
    value = Column(String(100)) 
    description = Column(Text, nullable=True)


    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")

class ProjectImage(Base):
    __tablename__ = "project_images"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(191), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="images")
    