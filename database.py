from sqlmodel import SQLModel, create_engine, Session

# تنظیمات اتصال به دیتابیس SQLite
DATABASE_URL = "sqlite:///./inventory.db"

# ایجاد موتور دیتابیس
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # برای دیباگ
)

def init_db():
    """ایجاد جداول دیتابیس بر اساس مدل‌های تعریف شده"""
    # فقط import مدل‌ها در داخل تابع
    from Models.user import User
    from Models.item import Item
    from Models.Provider import Provider
    from Models.supplier_order import SupplierOrder, SupplierOrderItem
    from Models.customer_order import CustomerOrder, CustomerOrderItem
    
    SQLModel.metadata.create_all(engine)
    print("✅ همه جداول ایجاد شدند")

def get_session():
   
    with Session(engine) as session:
        yield session