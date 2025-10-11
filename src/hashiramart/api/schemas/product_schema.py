from pydantic import BaseModel
from typing import Optional

# --- Base Schema ---
class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    weight: Optional[float] = None
    material: Optional[str] = None

# --- Create Schema ---
class ProductCreate(ProductBase):
    pass

# --- Update Schema ---
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    material: Optional[str] = None

# --- Read Schema ---
# RENAMED from Product to ProductSchema 👍
class ProductSchema(ProductBase):
    id: int

    class Config:
        from_attributes = True