from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import EmailStr
import bcrypt

# برای جلوگیری از circular imports
if TYPE_CHECKING:
    from .order import Order

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=30)
    email: EmailStr = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    role: str = Field(default="user")  # user, admin
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: Optional[str]=Field(default=None, min_length=8)
    hashed_password: str
    
    # Relationships - با استفاده از string type hints
    orders: List["Order"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserRead(UserBase):
    id: int
    role: str

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None