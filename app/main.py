from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import api_router

app = FastAPI(
    title="Warehouse AI Suite API",
    version="1.0.0",
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
