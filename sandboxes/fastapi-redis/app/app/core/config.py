from pydantic_settings import BaseSettings
from typing import Optional
import logging
from ddtrace import tracer

# Configure logging with Datadog format
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

# Configure logging with Datadog format
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.level = logging.INFO

# Configure exception logging to be more verbose
logging.getLogger('uvicorn.error').setLevel(logging.INFO)
logging.getLogger('uvicorn.access').setLevel(logging.INFO)

def setup_logging():
    return logger

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Application"
    API_V1_STR: str = "/api/v1"
    
    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 