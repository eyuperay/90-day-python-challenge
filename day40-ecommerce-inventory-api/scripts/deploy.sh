#!/bin/bash

echo "🚀 Day40 E-Commerce API Deployment Script"

# Build Docker image
echo "📦 Building Docker image..."
docker build -t day40-ecommerce-api -f docker/Dockerfile .

# Tag for AWS ECR (optional)
# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
# docker tag day40-ecommerce-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/day40-ecommerce-api:latest

# Push to ECR (optional)
# docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/day40-ecommerce-api:latest

echo "✅ Deployment completed!"