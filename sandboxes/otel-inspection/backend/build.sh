#!/bin/bash

# Registry details
REGISTRY="rcskin"
IMAGE_NAME="otel-inspection-backend"

# Build and push latest
echo "Building and pushing ${REGISTRY}/${IMAGE_NAME}:latest"
docker build -t ${REGISTRY}/${IMAGE_NAME}:latest .
docker push ${REGISTRY}/${IMAGE_NAME}:latest

echo "Done! Image pushed as: ${REGISTRY}/${IMAGE_NAME}:latest" 