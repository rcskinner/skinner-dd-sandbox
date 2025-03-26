from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Application"
    
    # Add your configuration variables here
    DATABASE_URL: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 