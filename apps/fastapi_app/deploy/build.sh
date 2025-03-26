#!/bin/bash

# Set variables
IMAGE_NAME="rcskin/fastapi-app"
IMAGE_TAG="latest"

# Login to Docker Hub
docker login

# Build the image
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f deploy/Dockerfile .

# Push to Docker Hub
docker push ${IMAGE_NAME}:${IMAGE_TAG} 