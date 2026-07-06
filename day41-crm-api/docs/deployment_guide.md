# CRM API - Deployment Guide

## Local Development

### Prerequisites
- Docker Desktop
- Python 3.11+

### Steps
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\Activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Start services: `docker-compose -f docker/docker-compose.yml up -d`
6. Seed database: `docker exec -it day41_app python scripts/seed_data.py`
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

## VPS Deployment (DigitalOcean/Linode)

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone and run
git clone https://github.com/yourusername/day41-crm-api.git
cd day41-crm-api
docker-compose -f docker/docker-compose.yml up -d