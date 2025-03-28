#!/bin/bash

# Build the Docker image
docker build -t rcskin/otel-store-frontend:latest .

# Push to Docker Hub
docker push rcskin/otel-store-frontend:latest

# Create namespace if it doesn't exist
kubectl apply -f ../../deploy/namespace.yaml

# Apply Kubernetes manifests
kubectl apply -f deploy/deployment.yaml
kubectl apply -f deploy/service.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=60s deployment/frontend -n otel-store

# Get the service URL
echo "Getting service URL..."
kubectl get service frontend -n otel-store 