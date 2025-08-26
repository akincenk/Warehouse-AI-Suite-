from fastapi import APIRouter
from . import skus, suppliers, inventory, purchase_orders, util

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(util.router, tags=["util"])
api_router.include_router(skus.router, prefix="/skus", tags=["skus"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["purchase_orders"])
