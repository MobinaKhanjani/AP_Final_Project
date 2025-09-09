from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .Provider import Provider
    from .item import Item

class SupplierOrderStatus(str, Enum):
    DRAFT = "draft"           # پیش‌نویس (ﺲﯾﻮﻧ ﺶﯿپ)
    SENT = "sent"             # ارسال شده (هﺪﺷ لﺎﺳرا)
    RECEIVED = "received"     # دریافت شده (هﺪﺷ ﻞیﻮﺤﺗ)
    CLOSED = "closed"         # بسته شده (هﺪﺷ ﻪتﺴﺑ)

class SupplierOrderBase(SQLModel):
    status: SupplierOrderStatus = Field(default=SupplierOrderStatus.DRAFT)
    notes: Optional[str] = Field(default=None, max_length=500)

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

# مدل واسط برای ارتباط بین SupplierOrder و Item
class SupplierOrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="supplierorder.id")
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0)  # تعداد (داﺪﻌﺗ)
    unit_price: float = Field(gt=0)  # قیمت واحد
    total_price: float = Field(gt=0)  # قیمت کل

class SupplierOrderItem(SupplierOrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    order: "SupplierOrder" = Relationship(back_populates="items")
    item: "Item" = Relationship(back_populates="supplier_order_items")