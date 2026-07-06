#!/bin/bash

echo "🚀 Day41 CRM API Deployment Script"

# Build Docker image
echo "📦 Building Docker image..."
docker build -t day41-crm-api -f docker/Dockerfile .

# Tag for AWS ECR (optional)
# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
# docker tag day41-crm-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/day41-crm-api:latest

# Push to ECR (optional)
# docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/day41-crm-api:latest

echo "✅ Deployment completed!"