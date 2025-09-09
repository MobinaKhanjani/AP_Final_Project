from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

# برای جلوگیری از circular imports
if TYPE_CHECKING:
    from .user import User
    from .item import Item

class OrderStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    RECEIVED = "received"
    CLOSED = "closed"

class OrderBase(SQLModel):
    status: OrderStatus = Field(default=OrderStatus.DRAFT)

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None

# مدل واسط برای ارتباط چند به چند بین Order و Item
class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0)
    expected_price: Optional[float] = Field(default=None, gt=0)

class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: Optional[int] = Field(foreign_key="transaction.id", default=None)
    
    # Relationships
    order: "Order" = Relationship(back_populates="items")
    item: "Item" = Relationship(back_populates="order_items")
    transaction: Optional["Transaction"] = Relationship(back_populates="order_item")

class OrderItemRead(OrderItemBase):
    id: int
    item: "Item"
    transaction: Optional["Transaction"] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(SQLModel):
    quantity: Optional[int] = None
    expected_price: Optional[float] = None
    transaction_id: Optional[int] = None