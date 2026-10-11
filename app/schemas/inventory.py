from pydantic import BaseModel, ConfigDict, Field


class InventoryBase(BaseModel):
    sku_id: int
    supplier_id: int | None = None
    on_hand: int = Field(0, ge=0)
    reorder_point: int = Field(10, ge=0)
    reorder_qty: int = Field(50, gt=0)


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    supplier_id: int | None = None
    on_hand: int | None = Field(None, ge=0)
    reorder_point: int | None = Field(None, ge=0)
    reorder_qty: int | None = Field(None, gt=0)


class InventoryOut(InventoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
