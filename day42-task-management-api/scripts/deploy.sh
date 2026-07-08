#!/usr/bin/env bash
set -e

echo "Running migrations/seed..."
python scripts/seed_data.py
echo "Starting app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000