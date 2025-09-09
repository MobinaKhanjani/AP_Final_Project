# Import تمام مدل‌ها برای دسترسی آسان‌تر
from .user import User, UserCreate, UserRead, UserUpdate
from .item import Item, ItemCreate, ItemRead, ItemUpdate
from .Provider import Provider, ProviderCreate, ProviderRead, ProviderUpdate
from .supplier_order import (
    SupplierOrder, 
    SupplierOrderCreate, 
    SupplierOrderRead, 
    SupplierOrderStatus
)

from .customer_order import (
    CustomerOrder,
    CustomerOrderCreate, 
    CustomerOrderRead, 
    CustomerOrderStatus
)
# لیست تمام مدل‌ها برای دسترسی عمومی
__all__ = [
    # User models
    'User', 'UserCreate', 'UserRead', 'UserUpdate',
    
    # Item models
    'Item', 'ItemCreate', 'ItemRead', 'ItemUpdate',
    
    # Provider models
    'Provider', 'ProviderCreate', 'ProviderRead', 'ProviderUpdate',
    
    'SupplierOrder', 'SupplierOrderCreate', 'SupplierOrderRead', 'SupplierOrderStatus',
    'CustomerOrder', 'CustomerOrderCreate', 'CustomerOrderRead', 'CustomerOrderStatus'
]

# همچنین می‌توانید توابع کمکی رو هم export کنید
from .user import User
from .item import Item

# توابع کاربردی
def get_all_table_models():
    """لیست تمام مدل‌های جدول (برای ایجاد جداول)"""
    from .user import User
    from .item import Item
    from .Provider import Provider
    from .supplier_order import SupplierOrder, SupplierOrderItem
    from .customer_order import CustomerOrder, CustomerOrderItem
    
    return [
        User,
        Item, 
        Provider,
        SupplierOrder,
        SupplierOrderItem,
        CustomerOrder,
        CustomerOrderItem
    ]