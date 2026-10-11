from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api import api_router
from app.core.auth import check_auth_config


@asynccontextmanager
async def lifespan(_app: FastAPI):
    check_auth_config()
    yield


app = FastAPI(
    title="Warehouse Inventory API",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "util", "description": "Utility endpoints"},
        {"name": "skus", "description": "SKUs CRUD"},
        {"name": "suppliers", "description": "Suppliers CRUD"},
        {"name": "inventory", "description": "Inventory and alerts"},
        {"name": "purchase_orders", "description": "Purchase orders CRUD"},
    ],
)

@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})

app.include_router(api_router)
