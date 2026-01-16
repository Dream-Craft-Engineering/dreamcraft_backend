from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .models import Base
from .routers import auth, users, blogs, roles, categories, tags, upload, dashboard, projects
from .core import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DreamCraft Engineering Backend")


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(blogs.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(projects.router)