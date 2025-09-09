from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

# برای جلوگیری از circular imports
if TYPE_CHECKING:
    from .user import User
    from .item import Item
    from .order import OrderItem




class Orderstatus(str,Enum):
     draft="draft"
     sent="sent"
     recived=" recived"
     closed="closed"
     
class TransactionBase(SQLModel):
    item_id: int = Field(foreign_key="item.id")
    quantity: int = Field(gt=0, description="تعداد باید بزرگتر از صفر باشد")
    transaction_type: TransactionType
    price: float
    status: Orderstatus = Field(default = Orderstatus.draft)

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
   
   # item: "Item" = Relationship(back_populates="transactions")
   # user: "User" = Relationship(back_populates="transactions")
    #order_item: Optional["OrderItem"] = Relationship(back_populates="transaction")

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    user_id: int
    item: "Item"

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(SQLModel):
    quantity: Optional[int] = None
    transaction_type: Optional[TransactionType] = None
    notes: Optional[str] = None
    
    #status update