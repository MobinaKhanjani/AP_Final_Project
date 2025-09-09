from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .item import Item

class CustomerOrderStatus(str, Enum):
    PENDING = "pending"        # در انتظار پرداخت
    PAID = "paid"              # پرداخت شده
    PROCESSING = "processing"  # در حال آماده‌سازی
    SHIPPED = "shipped"        # ارسال شده
    DELIVERED = "delivered"    # تحویل داده شده
    CANCELLED = "cancelled"    # لغو شده

class CustomerOrderBase(SQLModel):
    status: CustomerOrderStatus = Field(default=CustomerOrderStatus.PENDING)
    notes: Optional[str] = Field(default=None, max_length=500)
    total_price: Optional[float] = Field(default=0, ge=0)
    shipping_address: str  # آدرس ارسال
    payment_method: str    # روش پرداخت

class CustomerOrder(CustomerOrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
    user: "User" = Relationship(back_populates="customer_orders")
    items: List["CustomerOrderItem"] = Relationship(back_populates="order")

class CustomerOrderCreate(CustomerOrderBase):
    user_id: int

class CustomerOrderRead(CustomerOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

class CustomerOrderUpdate(SQLModel):
    status: Optional[CustomerOrderStatus] = None
    notes: Optional[str] = None
    total_price: Optional[float] = None
    shipping_address: Optional[str] = None
    payment_method: Optional[str] = None

# مدل واسط برای CustomerOrder و Item
class CustomerOrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="customerorder.id")
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    total_price: float = Field(gt=0)

class CustomerOrderItem(CustomerOrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    order: "CustomerOrder" = Relationship(back_populates="items")
    item: "Item" = Relationship(back_populates="customer_order_items")