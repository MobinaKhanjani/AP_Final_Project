from sqlmodel import Session
from models.provider import Provider  # مسیر دقیق فایل مدل‌ها رو تنظیم کن
from database import get_session

def delete_provider_by_id(provider_id: int) -> bool:
    """
    حذف تأمین‌کننده از دیتابیس بر اساس شناسه
    خروجی: True اگر حذف موفق بود، False اگر تأمین‌کننده پیدا نشد
    """
    session: Session = next(get_session())
    provider = session.get(Provider, provider_id)
    if provider:
        session.delete(provider)
        session.commit()
        session.close()
        return True
    session.close()
    return False
if __name__ == "__main__":
    provider_id = 1  # شناسه تأمین‌کننده‌ای که می‌خوای حذف کنی
    success = delete_provider_by_id(provider_id)
    if success:
        print("✅ تأمین‌کننده با موفقیت حذف شد.")
    else:
        print("❌ تأمین‌کننده‌ای با این شناسه پیدا نشد.")