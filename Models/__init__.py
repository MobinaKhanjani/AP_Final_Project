# Import تمام مدل‌ها برای دسترسی آسان‌تر
from .user import User, UserCreate, UserRead, UserUpdate
from .item import Item, ItemCreate, ItemRead, ItemUpdate
from .Provider import Provider, ProviderCreate, ProviderRead, ProviderUpdate
from .order import (
    Order, OrderCreate, OrderRead, OrderUpdate,
    OrderItem, OrderItemCreate, OrderItemRead, OrderItemUpdate,
    OrderStatus
)
from .transaction import (
    Transaction, TransactionCreate, TransactionRead, TransactionUpdate,
    TransactionType, TransactionStatus
)

# لیست تمام مدل‌ها برای دسترسی عمومی
__all__ = [
    # User models
    'User', 'UserCreate', 'UserRead', 'UserUpdate',
    
    # Item models
    'Item', 'ItemCreate', 'ItemRead', 'ItemUpdate',
    
    # Provider models
    'Provider', 'ProviderCreate', 'ProviderRead', 'ProviderUpdate',
    
    # Order models
    'Order', 'OrderCreate', 'OrderRead', 'OrderUpdate',
    'OrderItem', 'OrderItemCreate', 'OrderItemRead', 'OrderItemUpdate',
    'OrderStatus',
    
    # Transaction models
    'Transaction', 'TransactionCreate', 'TransactionRead', 'TransactionUpdate',
    'TransactionType', 'TransactionStatus'
]

# همچنین می‌توانید توابع کمکی رو هم export کنید
from .user import User
from .item import Item

# توابع کاربردی
def get_all_models():
    """لیست تمام مدل‌های جدول"""
    return [
        User,
        Item,
        Provider,
        Order,
        OrderItem,
        Transaction
    ]

def get_model_by_name(model_name: str):
    """دریافت مدل بر اساس نام"""
    models_dict = {
        'user': User,
        'item': Item,
        'provider': Provider,
        'order': Order,
        'order_item': OrderItem,
        'transaction': Transaction
    }
    return models_dict.get(model_name.lower())