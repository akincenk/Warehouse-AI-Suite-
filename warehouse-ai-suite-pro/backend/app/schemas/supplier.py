from pydantic import BaseModel, Field

class SupplierBase(BaseModel):
    name: str = Field(..., max_length=255)
    lead_time_days: int = 7

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: str | None = None
    lead_time_days: int | None = None

class SupplierOut(SupplierBase):
    id: int
    class Config:
        from_attributes = True
