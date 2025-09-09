from sqlmodel import SQLModel, create_engine, Session
from config import settings
from contextlib import contextmanager

# تنظیمات اتصال به دیتابیس SQLite
DATABASE_URL = "sqlite:///./inventory.db"

# ایجاد موتور دیتابیس
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

def init_db():
    """ایجاد جداول دیتابیس بر اساس مدل‌های تعریف شده"""
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    """Dependency برای FastAPI - مدیریت session با contextmanager"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()