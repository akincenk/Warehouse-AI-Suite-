import os

# Tests run against DATABASE_URL (PostgreSQL in CI). Without it, fall back to a local SQLite file.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import event  # noqa: E402

import app.models  # noqa: E402, F401
from app.db.session import Base, engine  # noqa: E402
from app.main import app  # noqa: E402

if engine.dialect.name == "sqlite":
    @event.listens_for(engine, "connect")
    def _enable_sqlite_fks(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

# No-op when Alembic has already created the schema (CI); creates it for SQLite runs.
Base.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def _clean_tables():
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sku(client):
    return client.post("/api/v1/skus", json={"code": "SKU-1", "name": "Widget", "category": "tools"}).json()


@pytest.fixture
def supplier(client):
    return client.post("/api/v1/suppliers", json={"name": "Acme", "lead_time_days": 5}).json()
