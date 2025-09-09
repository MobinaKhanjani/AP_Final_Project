from sqlmodel import select, Session
from Models.Provider import Provider
from Models.item import Item
from database import get_session

def delete_provider_by_id(provider_id: int) -> bool:
    """
    حذف تأمین‌کننده از دیتابیس.
    ابتدا کالاهای مرتبط بررسی می‌شوند.
    اگر کالا دارد، حذف انجام نمی‌شود.
    """
    session: Session = next(get_session())

    # بررسی وجود تأمین‌کننده
    provider = session.get(Provider, provider_id)
    if not provider:
        session.close()
        return False

    # بررسی کالاهای مرتبط
    statement = select(Item).where(Item.provider_id == provider_id)
    items = session.exec(statement).all()

    if items:
        print("⚠️ نمی‌توان تأمین‌کننده را حذف کرد چون کالاهای مرتبط دارد.")
        session.close()
        return False

    # حذف تأمین‌کننده
    session.delete(provider)
    session.commit()
    session.close()
    return True

# تست ساده
if __name__ == "__main__":
    provider_id = 1
    success = delete_provider_by_id(provider_id)
    if success:
        print("✅ تأمین‌کننده با موفقیت حذف شد.")
    else:
        print("❌ حذف انجام نشد. ممکن است تأمین‌کننده وجود نداشته باشد یا کالاهای وابسته داشته باشد.")
