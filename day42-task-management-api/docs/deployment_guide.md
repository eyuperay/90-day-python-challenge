# Deployment Guide

## Local
1. Copy `.env.example` to `.env`
2. Install dependencies
3. Run:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker
```bash
docker compose -f docker/docker-compose.yml up --build
```

## Seed data
```bash
python scripts/seed_data.py
```