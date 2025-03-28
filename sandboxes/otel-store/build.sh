#!/bin/bash

# Build and push frontend
echo "Building and pushing frontend..."
cd services/frontend
docker build --no-cache -t rcskin/otel-store-frontend:latest .
docker push rcskin/otel-store-frontend:latest
cd ../..

# Build and push inventory service
echo "Building and pushing inventory service..."
cd services/inventory-service-java
docker build --no-cache -t rcskin/otel-store-inventory-java:latest .
docker push rcskin/otel-store-inventory-java:latest
cd ../.. 