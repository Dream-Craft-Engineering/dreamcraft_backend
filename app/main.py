# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routers import auth, users, roles, blogs  # Import your routers
from .core import settings

app = FastAPI(title=settings.app_name)

# CORS middleware (allows Next.js to call APIs)
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

# For dev only: Create tables (comment out after initial setup; use Alembic for migrations)
# Base.metadata.create_all(bind=engine)