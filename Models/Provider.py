from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .item import Item

class ProviderBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    contact_person: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    delivery_time: Optional[int] = None

class Provider(ProviderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    items: List["Item"] = Relationship(back_populates="provider")

 # Relationships
    products: List["Item"] = Relationship(back_populates="provider")

class ProviderCreate(ProviderBase):
    pass

class ProviderRead(ProviderBase):
    id: int
    is_active: bool

class ProviderUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None