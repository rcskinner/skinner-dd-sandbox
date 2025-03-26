import redis
from app.core.config import settings

# Create Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True  # Automatically decode responses to strings
)

# Function to get Redis client
def get_redis():
    try:
        yield redis_client
    finally:
        pass  # Redis client is managed by the connection pool 