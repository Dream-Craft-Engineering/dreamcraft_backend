# backend/app/core.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")  # Ignore unknown env vars

    # Application config
    app_name: str = Field("DreamCraft Engineering Backend", env="APP_NAME")
    python_env: str = Field("development", env="PYTHON_ENV")

    # Database config
    database_url: str = Field(
        "mysql+pymysql://root:DreamCraft10@localhost:3306/dreamcraft_db", env="DATABASE_URL"
    )

    # CORS (for Next.js frontend)
    backend_cors_origins: List[str] = Field(default=["http://localhost:3000"], env="BACKEND_CORS_ORIGINS")

settings = Settings()