from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .item import Item
    from .order import Order

class TransactionType(str, Enum):
    INCOME = "income"    # درآمد (فروش محصول)
    EXPENSE = "expense"  # هزینه (خرید محصول)
    SALARY = "salary"    # حقوق
    OTHER = "other"      # سایر

class TransactionStatus(str, Enum):
    PENDING = "pending"    # در انتظار
    COMPLETED = "completed" # تکمیل شده
    FAILED = "failed"      # ناموفق

class TransactionBase(SQLModel):
    amount: float = Field(gt=0)
    transaction_type: TransactionType
    description: Optional[str] = Field(default=None, max_length=500)
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    order_id: Optional[int] = Field(foreign_key="order.id", default=None)
    item_id: Optional[int] = Field(foreign_key="item.id", default=None)
    
    # Relationships
    user: "User" = Relationship(back_populates="transactions")
    order: Optional["Order"] = Relationship(back_populates="transactions")
    item: Optional["Item"] = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    user_id: int
    order_id: Optional[int] = None
    item_id: Optional[int] = None

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    order_id: Optional[int]
    item_id: Optional[int]

class TransactionUpdate(SQLModel):
    amount: Optional[float] = None
    transaction_type: Optional[TransactionType] = None
    description: Optional[str] = None
    status: Optional[TransactionStatus] = None