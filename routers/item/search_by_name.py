from sqlmodel import select, Session
from models.item import Item
from database import get_session

def search_items_by_name(name_query: str) -> list[Item]:
    """
    جستجوی کالاها بر اساس نام (جستجوی جزئی و حساس به حروف)
    """
    session: Session = next(get_session())
    statement = select(Item).where(Item.name.contains(name_query))
    results = session.exec(statement).all()
    session.close()
    return results
if __name__ == "__main__":
    name_input = "کابل"  # بخشی از نام کالا
    items = search_items_by_name(name_input)
    if items:
        print(f"✅ {len(items)} کالا پیدا شد:")
        for item in items:
            print(f"- {item.name} | قیمت: {item.price} | موجودی: {item.quantity}")
    else:
        print("❌ هیچ کالایی با این نام پیدا نشد.")
