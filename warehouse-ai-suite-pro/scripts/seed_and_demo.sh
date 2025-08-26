#!/usr/bin/env bash
set -euo pipefail
docker compose -f infra/docker-compose.yml up -d --build
docker compose -f infra/docker-compose.yml exec api alembic upgrade head
docker compose -f infra/docker-compose.yml exec api python -m app.seed.seed_demo
curl -s http://localhost:8000/health
