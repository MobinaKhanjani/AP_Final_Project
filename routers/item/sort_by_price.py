from sqlmodel import select, Session
from models.item import Item
from database import get_session
def get_items_sorted_by_price(descending: bool = False) -> list[Item]:
    """
    دریافت لیست کالاها مرتب‌شده بر اساس قیمت
    :param descending: اگر True باشد، مرتب‌سازی نزولی انجام می‌شود
    """
    session: Session = next(get_session())
    order = Item.price.desc() if descending else Item.price.asc()
    statement = select(Item).order_by(order)
    results = session.exec(statement).all()
    session.close()
    return results
if __name__ == "__main__":
    items = get_items_sorted_by_price(descending=False)
    print("📦 لیست کالاها مرتب‌شده بر اساس قیمت:")
    for item in items:
        print(f"{item.name} | قیمت: {item.price} | موجودی: {item.quantity}")