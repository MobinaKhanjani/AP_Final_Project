from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .item import Item
    from .transaction import Transaction

class OrderStatus(str, Enum):
    DRAFT = "draft"       # پیش‌نویس
    SENT = "sent"         # ارسال شده
    RECEIVED = "received" # دریافت شده
    CLOSED = "closed"     # بسته شده

class OrderBase(SQLModel):
    status: OrderStatus = Field(default=OrderStatus.DRAFT)
    notes: Optional[str] = Field(default=None, max_length=500)
    total_price: Optional[float] = Field(default=0, ge=0)

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    transactions: List["Transaction"] = Relationship(back_populates="order")

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    total_price: float

class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None
    total_price: Optional[float] = None

# مدل واسط برای ارتباط چند به چند بین Order و Item
class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    total_price: float = Field(gt=0)

class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    order: "Order" = Relationship(back_populates="items")
    item: "Item" = Relationship(back_populates="order_items")