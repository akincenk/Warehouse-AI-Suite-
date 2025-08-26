#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Launching stack..."
docker compose -f infra/docker-compose.yml up -d --build

echo "[2/5] Running migrations..."
docker compose -f infra/docker-compose.yml exec api alembic upgrade head

echo "[3/5] Seeding demo data..."
docker compose -f infra/docker-compose.yml exec api python -m app.seed.seed_demo

echo "[4/5] Health check:"
curl -s http://localhost:8000/health | jq . || curl -s http://localhost:8000/health

echo "[5/5] Sample queries:"
echo "List SKUs:"
curl -s http://localhost:8000/api/v1/skus | jq . || curl -s http://localhost:8000/api/v1/skus

echo "Low stock alerts:"
curl -s http://localhost:8000/api/v1/inventory/alerts/low-stock | jq . || curl -s http://localhost:8000/api/v1/inventory/alerts/low-stock

echo "Open API docs: http://localhost:8000/docs"
