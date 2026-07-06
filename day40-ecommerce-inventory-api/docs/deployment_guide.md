# Deployment Guide

## Local Development

### Prerequisites
- Docker Desktop
- Python 3.11+

### Steps
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\Activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start services: `docker-compose -f docker/docker-compose.yml up -d`
6. Seed database: `docker exec -it day40_app python scripts/seed_data.py`
7. Access API: `http://localhost:8000`

## AWS Deployment

### Prerequisites
- AWS Account
- AWS CLI configured
- Docker

### Steps
1. Create RDS PostgreSQL instance
2. Create ElastiCache Redis cluster
3. Build Docker image
4. Push to ECR
5. Deploy to ECS

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Set to "False" in production