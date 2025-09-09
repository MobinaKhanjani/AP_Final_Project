from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .Provider import Provider
    from .item import Item

class SupplierOrderStatus(str, Enum):
    DRAFT = "draft"           # پیش‌نویس
    ORDERED = "ordered"       # سفارش داده شده
    CONFIRMED = "confirmed"   # تایید توسط تامین‌کننده
    SHIPPED = "shipped"       # ارسال شده
    RECEIVED = "received"     # دریافت در انبار
    CANCELLED = "cancelled"   # لغو شده

class SupplierOrderBase(SQLModel):
    status: SupplierOrderStatus = Field(default=SupplierOrderStatus.DRAFT)
    notes: Optional[str] = Field(default=None, max_length=500)
    total_price: Optional[float] = Field(default=0, ge=0)
    expected_delivery: datetime  # تاریخ تحویل预期
    actual_delivery: Optional[datetime] = None  # تاریخ تحویل واقعی

class SupplierOrder(SupplierOrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    provider_id: int = Field(foreign_key="provider.id")
    
    # Relationships
    provider: "Provider" = Relationship(back_populates="supplier_orders")
    items: List["SupplierOrderItem"] = Relationship(back_populates="order")

class SupplierOrderCreate(SupplierOrderBase):
    provider_id: int

class SupplierOrderRead(SupplierOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    provider_id: int

class SupplierOrderUpdate(SQLModel):
    status: Optional[SupplierOrderStatus] = None
    notes: Optional[str] = None
    total_price: Optional[float] = None
    expected_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None

# مدل واسط برای SupplierOrder و Item
class SupplierOrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="supplierorder.id")
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    total_price: float = Field(gt=0)

class SupplierOrderItem(SupplierOrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    order: "SupplierOrder" = Relationship(back_populates="items")
    item: "Item" = Relationship(back_populates="supplier_order_items")