#!/bin/bash

# Exit on error
set -e

echo "🚀 Building and deploying applications..."

# Build and push FastAPI image
echo "📦 Building FastAPI image..."
cd fastapi_app
docker build --no-cache -t rcskin/fastapi-app:latest -f deploy/Dockerfile .
docker push rcskin/fastapi-app:latest
cd ..

# Build and push loadtest image
echo "📦 Building loadtest image..."
cd loadtest
docker build --no-cache -t rcskin/loadtest:latest .
docker push rcskin/loadtest:latest
cd ..

echo "✅ Deployment complete!" 