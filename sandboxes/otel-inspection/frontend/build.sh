#!/bin/bash

# Build the image
docker build -t rcskin/otel-inspection-frontend:latest .

# Push the image
docker push rcskin/otel-inspection-frontend:latest 