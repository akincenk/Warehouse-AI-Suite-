# Warehouse AI Suite: Inventory API

[![CI](https://github.com/akincenk/Warehouse-AI-Suite-/actions/workflows/ci.yml/badge.svg)](https://github.com/akincenk/Warehouse-AI-Suite-/actions/workflows/ci.yml)

A REST backend for warehouse inventory: SKUs, suppliers, stock levels, purchase orders and low-stock alerts.

> **About the name:** there is no AI or machine learning in this repository yet. It is the inventory data layer
> that forecasting or replenishment models would sit on top of; those are listed under *Next steps*.

## What it does

- CRUD for **SKUs**, **suppliers**, **inventory rows** (stock per SKU, optional supplier) and **purchase orders**.
- **Low-stock alerts**: `GET /api/v1/inventory/alerts/low-stock` returns every inventory row whose `on_hand` is at or
  below its `reorder_point`.
- Input validation: duplicate SKU codes / supplier names return `409`, unknown IDs return `404`, references to a
  non-existent SKU or supplier return `400`, negative quantities and unknown PO statuses return `422`.
- Referential integrity in the database: deleting a SKU deletes its inventory rows and purchase orders; deleting a
  supplier unlinks it from inventory rows.

## Stack

FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL 16, Docker Compose, pytest, ruff, GitHub Actions.

```
app/
  main.py            FastAPI app, /health
  api/               routers: skus, suppliers, inventory, purchase_orders, util (/ping)
  models/            SQLAlchemy models
  schemas/           Pydantic request/response models
  db/session.py      engine, session, Base
  db/migrations/     Alembic environment and versions
  core/settings.py   configuration from environment variables
tests/               API tests (TestClient)
```

```mermaid
erDiagram
  SKU ||--o{ Inventory : stocked_as
  Supplier |o--o{ Inventory : supplies
  SKU ||--o{ PurchaseOrder : ordered_as
```

## Quickstart

### Docker Compose

```bash
docker compose up -d --build      # starts Postgres, applies migrations, serves the API on :8000
curl http://localhost:8000/health
open http://localhost:8000/docs    # interactive OpenAPI docs
docker compose down -v             # stop and delete the database volume
```

Database credentials default to dev-only `postgres/postgres`; override them with `POSTGRES_USER`, `POSTGRES_PASSWORD`
and `POSTGRES_DB` in a `.env` file (see `.env.example`).

### Local (Python 3.11+)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/warehouse   # any reachable Postgres
alembic upgrade head
uvicorn app.main:app --reload
```

## Configuration

| Variable       | Default (dev only)                                                  |
|----------------|---------------------------------------------------------------------|
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres@localhost:5432/warehouse`   |

Used by both the app and Alembic.

## API overview

All resource routes are under `/api/v1`. Full schemas at `/docs`.

| Method | Path | Notes |
|---|---|---|
| GET | `/health`, `/api/v1/ping` | liveness |
| GET, POST | `/skus` | `409` on duplicate `code` |
| GET, PUT, DELETE | `/skus/{id}` | `code` is immutable |
| GET, POST | `/suppliers` | `409` on duplicate `name` |
| PUT, DELETE | `/suppliers/{id}` | |
| GET, POST | `/inventory` | `400` if `sku_id` / `supplier_id` does not exist |
| PUT, DELETE | `/inventory/{id}` | |
| GET | `/inventory/alerts/low-stock` | rows with `on_hand <= reorder_point` |
| GET, POST | `/purchase-orders` | `status` is `created`, `sent` or `received` |
| PUT, DELETE | `/purchase-orders/{id}` | |

```bash
curl -X POST localhost:8000/api/v1/skus -H 'content-type: application/json' -d '{"code":"BOLT-M8","name":"M8 bolt"}'
curl -X POST localhost:8000/api/v1/inventory -H 'content-type: application/json' -d '{"sku_id":1,"on_hand":4,"reorder_point":10}'
curl localhost:8000/api/v1/inventory/alerts/low-stock
```

## Tests

```bash
pytest
```

Tests use `DATABASE_URL` if set; otherwise they fall back to a local SQLite file so they run without Postgres. CI runs
them against PostgreSQL 16 on Python 3.11 and 3.12 after `alembic upgrade head`, and runs `alembic check` to fail if
the models and migrations drift apart. It also lints with ruff and builds the Docker image.

## Limitations and next steps

- No authentication or authorization; do not expose it publicly as is.
- No pagination or filtering on list endpoints.
- Purchase orders do not change stock levels when received, and status transitions are not enforced.
- Low-stock alerts are a pull endpoint; there is no notification channel.
- Possible next steps, including the "AI" the name points at: demand forecasting per SKU, reorder-quantity
  suggestions from supplier lead times, and a small dashboard.

## License

MIT, see [LICENSE](LICENSE).
