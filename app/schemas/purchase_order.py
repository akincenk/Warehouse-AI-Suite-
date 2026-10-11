from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

POStatus = Literal["created", "sent", "received"]


class POBase(BaseModel):
    sku_id: int
    qty: int = Field(..., gt=0)
    status: POStatus = "created"


class POCreate(POBase):
    pass


class POUpdate(BaseModel):
    qty: int | None = Field(None, gt=0)
    status: POStatus | None = None


class POOut(POBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
