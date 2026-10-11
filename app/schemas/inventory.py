from pydantic import BaseModel

class InventoryBase(BaseModel):
    sku_id: int
    supplier_id: int | None = None
    on_hand: int = 0
    reorder_point: int = 10
    reorder_qty: int = 50

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    supplier_id: int | None = None
    on_hand: int | None = None
    reorder_point: int | None = None
    reorder_qty: int | None = None

class InventoryOut(InventoryBase):
    id: int
    class Config:
        from_attributes = True
