from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    lead_time_days: int = Field(7, ge=0)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    lead_time_days: int | None = Field(None, ge=0)


class SupplierOut(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
