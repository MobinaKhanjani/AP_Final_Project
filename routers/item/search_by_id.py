from sqlmodel import Session
from models.item import Item
from database import get_session

def search_item_by_id(item_id: int) -> Item | None:
    """
    جستجوی محصول بر اساس شناسه (ID)
    """
    session: Session = next(get_session())
    item = session.get(Item, item_id)
    session.close()
    return item
if __name__ == "__main__":
    item_id = 1  # شناسه‌ای که می‌خوای جستجو کنی
    item = search_item_by_id(item_id)
    if item:
        print(f"✅ محصول پیدا شد:")
        print(f"نام: {item.name}")
        print(f"قیمت: {item.price}")
        print(f"موجودی: {item.quantity}")
        print(f"شناسه تأمین‌کننده: {item.provider_id}")
        print(f"تاریخ ایجاد: {item.created_at}")
    else:
        print("❌ محصولی با این شناسه پیدا نشد.")