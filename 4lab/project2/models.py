from pydantic import BaseModel, Field
from typing import Optional

class StoreAdd(BaseModel):
    name: str
    address: str

class StoreResponse(BaseModel):
    id: int
    name: str
    address: str

class ProductAdd(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    store_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    store_id: int