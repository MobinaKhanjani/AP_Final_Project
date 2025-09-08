from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class ItemBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    sku: str = Field(index=True, unique=True, max_length=50)
    price: float = Field(gt=0, description="قیمت باید بزرگتر از صفر باشد")
    quantity: int = Field(default=0, ge=0, description="تعداد موجودی نمی‌تواند منفی باشد")
    min_threshold: int = Field(default=5, ge=0, description="حداقل موجودی برای هشدار")
    location: Optional[str] = Field(default=None, max_length=100, description="محل قرارگیری در انبار")

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationships
    transactions: List["Transaction"] = Relationship(back_populates="item")
    order_items: List["OrderItem"] = Relationship(back_populates="item")

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    min_threshold: Optional[int] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None

# برای جلوگیری از خطاهای circular import
from .transaction import Transaction
from .order import OrderItem