#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Deploying Day43 Booking System API..."

# Build and start containers
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for DB to be ready
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
docker-compose exec api alembic upgrade head
echo "✓ Migrations applied"

# Optional: seed demo data
if [[ "${SEED_DATA:-false}" == "true" ]]; then
    docker-compose exec api python scripts/seed.py
    echo "✓ Demo data seeded"
fi

echo ""
echo "✅ API is running at http://localhost:8000"
echo "📖 Docs: http://localhost:8000/docs"
