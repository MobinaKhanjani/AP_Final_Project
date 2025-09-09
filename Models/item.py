from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .order import OrderItem
    from .transaction import Transaction
    from .Provider import Provider

class ItemBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    sku: str = Field(index=True, unique=True, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(default=0, ge=0)
    min_threshold: int = Field(default=5, ge=0)
    provider_id: int = Field(foreign_key="provider.id")

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    order_items: List["OrderItem"] = Relationship(back_populates="item")
    transactions: List["Transaction"] = Relationship(back_populates="item")
    provider: "Provider" = Relationship(back_populates="items")
    
class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    min_threshold: Optional[int] = None

# برای جلوگیری از خطاهای circular import
from .transaction import Transaction
from .order import OrderItem