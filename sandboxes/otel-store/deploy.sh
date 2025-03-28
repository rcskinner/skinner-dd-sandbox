#!/bin/bash

# Build and push frontend
cd services/frontend
docker build -t rcskin/otel-store-frontend:latest .
docker push rcskin/otel-store-frontend:latest
cd ../..

# Build and push inventory service
cd services/inventory-service
docker build -t rcskin/otel-store-inventory:latest .
docker push rcskin/otel-store-inventory:latest
cd ../..

# Apply kustomize
kubectl apply -k .

# Restart deployments
kubectl rollout restart deployment frontend -n otel-store
kubectl rollout restart deployment inventory-service -n otel-store 