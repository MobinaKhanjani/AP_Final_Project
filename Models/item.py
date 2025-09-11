from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .supplier_order import SupplierOrderItem
    from .customer_order import CustomerOrderItem
    from .Provider import Provider

class ItemBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    sku: str = Field(index=True, unique=True, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(default=0, ge=0)
    min_threshold: int = Field(default=5, ge=0)
    provider_id: int = Field(foreign_key="provider.id")
    notes: Optional[str] = Field(default=None, max_length=500)

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    provider: "Provider" = Relationship(back_populates="items")
    supplier_order_items: List["SupplierOrderItem"] = Relationship(back_populates="item")
    customer_order_items: List["CustomerOrderItem"] = Relationship(back_populates="item")
    
class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    min_threshold: Optional[int] = None

