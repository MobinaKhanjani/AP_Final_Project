from sqlmodel import select, Session
from models.item import Item
from database import get_session

def search_item_by_sku(sku: str) -> Item | None:
    """
    جستجوی کالا بر اساس شناسه SKU
    """
    session: Session = next(get_session())
    statement = select(Item).where(Item.sku == sku)
    result = session.exec(statement).first()
    session.close()
    return result
if __name__ == "__main__":
    sku_input = "ABC123"  # مقدار SKU که می‌خوای جستجو کنی
    item = search_item_by_sku(sku_input)
    if item:
        print("✅ کالا پیدا شد:")
        print(f"نام: {item.name}")
        print(f"قیمت: {item.price}")
        print(f"موجودی: {item.quantity}")
        print(f"تأمین‌کننده: {item.provider_id}")
    else:
        print("❌ کالایی با این SKU پیدا نشد.")