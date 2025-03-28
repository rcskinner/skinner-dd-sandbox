#!/bin/bash

# Apply kustomize
kubectl apply -k .

# Restart deployments
kubectl rollout restart deployment frontend -n otel-store
kubectl rollout restart deployment inventory-service -n otel-store 