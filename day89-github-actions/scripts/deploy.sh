#!/bin/bash
# Deployment script for CI/CD

echo "=========================================="
echo "Deploying Application"
echo "=========================================="

# Set environment variables
export APP_VERSION=${GITHUB_SHA:0:7}
export APP_ENV=production

# Pull latest image
docker pull $DOCKER_USERNAME/my-app:latest

# Stop and remove old container
docker stop my-app || true
docker rm my-app || true

# Run new container
docker run -d \
  --name my-app \
  -p 80:5000 \
  -e APP_VERSION=$APP_VERSION \
  -e APP_ENV=production \
  $DOCKER_USERNAME/my-app:latest

echo "=========================================="
echo "Deployment Complete!"
echo "Version: $APP_VERSION"
echo "=========================================="
