from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import EmailStr, validator
import bcrypt

if TYPE_CHECKING:
    from .customer_order import CustomerOrder

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=30)
    email: EmailStr = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    role: str = Field(default="user")
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    #Relationship
    customer_orders: List["CustomerOrder"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """بررسی قدرت رمز عبور"""
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        return True

# کلاس‌های جدید اضافه شده
class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = Field(default="user")

    @validator('password')
    def validate_password(cls, v):
        if not User.validate_password_strength(v):
            raise ValueError("رمز عبور باید حداقل ۸ کاراکتر و شامل حروف و اعداد باشد")
        return v

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('password')
    def validate_password(cls, v):
        if v is not None and not User.validate_password_strength(v):
            raise ValueError("رمز عبور باید حداقل ۸ کاراکتر و شامل حروف و اعداد باشد")
        return v
