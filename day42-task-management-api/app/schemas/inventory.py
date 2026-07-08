from pydantic import BaseModel, ConfigDict


class InventoryCreate(BaseModel):
    name: str
    sku: str
    quantity: int = 0
    location: str | None = None


class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    quantity: int
    location: str | None = None