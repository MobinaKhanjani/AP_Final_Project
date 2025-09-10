from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum
from .user import User

if TYPE_CHECKING:
    from .user import User
    from .item import Item

class CustomerOrderStatus(str, Enum):
    PENDING = "pending"    # در انتظار
    PAID = "paid"          # پرداخت شده
    SHIPPED = "shipped"    # ارسال شده
    DELIVERED = "delivered" # تحویل داده شده

class CustomerOrderBase(SQLModel):
    status: CustomerOrderStatus = Field(default=CustomerOrderStatus.PENDING)

class CustomerOrder(CustomerOrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
    user: "User" = Relationship(back_populates="customer_orders")
    items: List["CustomerOrderItem"] = Relationship(back_populates="order")

# مدل واسط برای ارتباط بین CustomerOrder و Item
class CustomerOrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="customerorder.id")
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0)  # تعداد

class CustomerOrderItem(CustomerOrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    order: "CustomerOrder" = Relationship(back_populates="items")
    item: "Item" = Relationship(back_populates="customer_order_items")
    
class CustomerOrderCreate(CustomerOrderBase):
    user_id: int
    items: List["CustomerOrderItemBase"]

class CustomerOrderRead(CustomerOrderBase):
    id: int
    created_at: datetime
    user_id: int
    items: List["CustomerOrderItem"]

class CustomerOrderUpdate(SQLModel):
    status: Optional[CustomerOrderStatus] = None
    items: Optional[List["CustomerOrderItemBase"]] = None