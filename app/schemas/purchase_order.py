from pydantic import BaseModel

class POBase(BaseModel):
    sku_id: int
    qty: int
    status: str = "created"

class POCreate(POBase):
    pass

class POUpdate(BaseModel):
    qty: int | None = None
    status: str | None = None

class POOut(POBase):
    id: int
    class Config:
        from_attributes = True
