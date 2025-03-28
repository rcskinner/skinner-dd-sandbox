#!/bin/bash

# Exit on error
set -e

echo "🚀 Deploying applications to Kubernetes..."

# Deploy FastAPI application
echo "📦 Deploying FastAPI application..."
kubectl apply -k fastapi_app/deploy/k8s/
echo "🔄 Restarting FastAPI deployment..."
kubectl rollout restart deployment fastapi-app -n pyapp

# Deploy loadtest application
echo "📦 Deploying loadtest application..."
kubectl apply -k loadtest/k8s/
echo "🔄 Restarting loadtest deployment..."
kubectl rollout restart deployment api-load-test -n pyapp

echo "✅ Kubernetes deployment complete!" 