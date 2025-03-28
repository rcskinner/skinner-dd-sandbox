from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings, setup_logging
from app.core.database import get_redis
from typing import List
import json
import redis
from ddtrace import tracer

# Setup logging
logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI application with Redis database",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to FastAPI application with Redis"}

@app.get("/health")
async def health_check():
    logger.info("Health check called")
    return {"status": "healthy"}

@app.get("/items/", response_model=List[dict])
async def get_items(redis_client: redis.Redis = Depends(get_redis)):
    """Get all items from Redis"""
    logger.info("Getting all items")
    items = []
    for key in redis_client.keys("item:*"):
        item_data = redis_client.get(key)
        if item_data:
            items.append(json.loads(item_data))
    logger.info(f"Found {len(items)} items")
    return items

@app.post("/items/", response_model=dict)
async def create_item(name: str, description: str, redis_client: redis.Redis = Depends(get_redis)):
    """Create a new item in Redis"""
    logger.info("Creating new item")
    # Generate a new ID (in production, use a proper ID generator)
    item_id = str(redis_client.incr("item:counter"))
    item = {
        "id": item_id,
        "name": name,
        "description": description
    }
    redis_client.set(f"item:{item_id}", json.dumps(item))
    logger.info(f"Created item with ID: {item_id}")
    return item

@app.get("/items/{item_id}", response_model=dict)
async def get_item(item_id: str, redis_client: redis.Redis = Depends(get_redis)):
    """Get a specific item by ID"""
    logger.info(f"Getting item with ID: {item_id}")
    item_data = redis_client.get(f"item:{item_id}")
    if item_data is None:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Found item: {item_id}")
    return json.loads(item_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 