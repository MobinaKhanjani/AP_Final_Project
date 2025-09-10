from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .item import Item
    from .order import Order

class ProviderBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    contact_person: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)

class Provider(ProviderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # فیلد برای امتیازدهی⭐
    delivery_time_rating: Optional[int] = Field(default=None, ge=1, le=5)  # امتیاز سرعت تحویل (1-5)
    delivery_accuracy_score: Optional[int] = Field(default=None, ge=0, le=100)  # امتیاز صحت تحویل (0-100)
    orders: List["Order"] = Relationship(back_populates="provider")
    # Relationships - فقط یک رابطه داشته باش
    #chera?
    items: List["Item"] = Relationship(back_populates="provider")

class ProviderCreate(ProviderBase):
    pass

class ProviderRead(ProviderBase):
    id: int
    is_active: bool
    created_at: datetime
    delivery_time_rating: Optional[int]  
    delivery_accuracy_score: Optional[int]  

class ProviderUpdate(SQLModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    delivery_time_rating: Optional[int] = None 
    delivery_accuracy_score: Optional[int] = None  