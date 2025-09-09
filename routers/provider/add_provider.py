from sqlmodel import Session
from models.provider import Provider  # مسیر دقیق فایل مدل‌ها رو تنظیم کن
from database import get_session

def add_provider(name: str, contact_info: str = "", address: str = "") -> Provider:
    """
    افزودن تأمین‌کننده جدید به دیتابیس
    """
    session: Session = next(get_session())
    provider = Provider(name=name, contact_info=contact_info, address=address)
    session.add(provider)
    session.commit()
    session.refresh(provider)
    session.close()
    return provider
if __name__ == "__main__":
    new_provider = add_provider(
        name="شرکت توسعه کالا",
        contact_info="021-12345678",
        address="تهران، خیابان ولیعصر، پلاک 42"
    )
    print(f"✅ تأمین‌کننده اضافه شد:")
    print(f"نام: {new_provider.name}")
    print(f"تماس: {new_provider.contact_info}")
    print(f"آدرس: {new_provider.address}")