from fastapi import APIRouter, Depends

from app.core.auth import require_api_key

from . import inventory, purchase_orders, skus, suppliers, util

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(util.router, tags=["util"])

_protected = [Depends(require_api_key)]
api_router.include_router(skus.router, prefix="/skus", tags=["skus"], dependencies=_protected)
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"], dependencies=_protected)
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"], dependencies=_protected)
api_router.include_router(
    purchase_orders.router, prefix="/purchase-orders", tags=["purchase_orders"], dependencies=_protected
)
