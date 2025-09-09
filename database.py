from sqlmodel import SQLModel, create_engine, Session

# تنظیمات اتصال به دیتابیس SQLite
DATABASE_URL = "sqlite:///./inventory.db"

# ایجاد موتور دیتابیس
engine = create_engine( 
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # مورد نیاز برای SQLite
    echo=True  # نمایش کوئری‌ها در کنسول برای دیباگ (در production غیرفعال کنید)
)

def init_db():
    """ایجاد جداول دیتابیس بر اساس مدل‌های تعریف شده"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """دependencies برای ارائه session به routeها"""
    with Session(engine) as session:
        yield session