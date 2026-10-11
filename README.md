# Warehouse Inventory API

[![CI](https://github.com/akincenk/warehouse-inventory-api/actions/workflows/ci.yml/badge.svg)](https://github.com/akincenk/warehouse-inventory-api/actions/workflows/ci.yml)

A REST backend for warehouse inventory: SKUs, suppliers, stock levels, purchase orders and low-stock alerts.

There is no AI or machine learning in this repository. It is the inventory data layer that forecasting or
replenishment models could sit on top of (see *Limitations and next steps*).

## What it does

- CRUD for **SKUs**, **suppliers**, **inventory rows** (stock per SKU, optional supplier) and **purchase orders**.
- **Low-stock alerts**: `GET /api/v1/inventory/alerts/low-stock` returns every inventory row whose `on_hand` is at or
  below its `reorder_point`.
- API-key authentication on every resource route (`X-API-Key` header).
- Input validation: duplicate SKU codes / supplier names return `409` (also under concurrent inserts, via the
  database unique constraint), unknown IDs return `404`, references to a
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
  core/auth.py       X-API-Key check and startup guard
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
git clone https://github.com/akincenk/warehouse-inventory-api.git && cd warehouse-inventory-api
cp .env.example .env               # then set API_KEY (and real Postgres credentials) in .env
docker compose up -d --build      # starts Postgres, applies migrations, serves the API on :8000
curl http://localhost:8000/health
open http://localhost:8000/docs    # interactive OpenAPI docs
docker compose down -v             # stop and delete the database volume
```

Database credentials default to dev-only `postgres/postgres`; override them with `POSTGRES_USER`, `POSTGRES_PASSWORD`
and `POSTGRES_DB` in `.env`. Postgres is not published to the host; only the `api` container can reach it.

### Local (Python 3.11+)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/warehouse   # any reachable Postgres
export API_KEY=dev-key             # or ALLOW_NO_AUTH=true for local experiments only
alembic upgrade head
uvicorn app.main:app --reload
```

## Configuration

| Variable       | Default (dev only)                                                  |
|----------------|---------------------------------------------------------------------|
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres@localhost:5432/warehouse`   |
| `API_KEY`      | none; required unless `ALLOW_NO_AUTH=true`                          |
| `ALLOW_NO_AUTH`| `false`; `true` disables the API-key check (local development only)  |

`DATABASE_URL` is used by both the app and Alembic. The app refuses to start if `API_KEY` is empty and
`ALLOW_NO_AUTH` is not `true`.

## API overview

All resource routes are under `/api/v1` and require the `X-API-Key` header (`401` otherwise); `/health` and
`/api/v1/ping` are public. Full schemas at `/docs`.

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
H='X-API-Key: dev-key'
curl -X POST localhost:8000/api/v1/skus -H "$H" -H 'content-type: application/json' -d '{"code":"BOLT-M8","name":"M8 bolt"}'
curl -X POST localhost:8000/api/v1/inventory -H "$H" -H 'content-type: application/json' -d '{"sku_id":1,"on_hand":4,"reorder_point":10}'
curl -H "$H" localhost:8000/api/v1/inventory/alerts/low-stock
```

## Tests

```bash
pytest
```

Tests use `DATABASE_URL` if set; otherwise they fall back to a local SQLite file so they run without Postgres. Pytest
treats warnings as errors. CI runs the tests against PostgreSQL 16 on Python 3.11 and 3.12 after `alembic upgrade head`,
and runs `alembic check` to fail if the models and migrations drift apart. It also lints with ruff, audits
dependencies with `pip-audit`, and builds the Docker image. Dependabot proposes weekly pip and Actions updates.

## Design decisions

- **Synchronous SQLAlchemy with plain `def` handlers.** FastAPI runs them in its threadpool, so blocking DB calls do
  not stall the event loop, and the code stays simple.
- **Uniqueness enforced by the database.** Handlers pre-check for a friendly `409`, but the unique constraint is the
  real guard: an `IntegrityError` from a concurrent insert is also turned into `409`.
- **Alembic is the schema source of truth.** CI fails if models and migrations diverge (`alembic check`).
- **Runtime dependencies are pinned exactly** in `pyproject.toml`; test and lint tools live in the `dev` extra.

## Security

- A single shared API key (`X-API-Key`), compared in constant time. The app will not start without one unless
  `ALLOW_NO_AUTH=true` is set explicitly.
- No secrets in the repository; configuration comes from the environment (`.env.example` holds dev-only values).
- The Docker image runs as a non-root user; Compose does not expose Postgres outside its network.
- Pydantic validates all request bodies (lengths, non-negative quantities, allowed PO statuses).

## Limitations and next steps

- One shared API key, no per-user accounts, roles or key rotation; put it behind TLS.
- No pagination or filtering on list endpoints.
- Purchase orders do not change stock levels when received, and status transitions are not enforced.
- Low-stock alerts are a pull endpoint; there is no notification channel.
- Possible next steps, including the "AI" the name points at: demand forecasting per SKU, reorder-quantity
  suggestions from supplier lead times, and a small dashboard.

## License

MIT, see [LICENSE](LICENSE).
