from sqlmodel import Session
from models.provider import Provider
from database import get_session

def add_provider(
    name: str,
    contact_person: str = "",
    email: str = "",
    phone: str = "",
    delivery_time: int = 0
) -> Provider:
    """
    افزودن تأمین‌کننده جدید به دیتابیس
    """
    session: Session = next(get_session())
    provider = Provider(
        name=name,
        contact_person=contact_person,
        email=email,
        phone=phone,
        delivery_time=delivery_time
    )
    session.add(provider)
    session.commit()
    session.refresh(provider)
    session.close()
    return provider
if __name__ == "__main__":
    new_provider = add_provider(
        name="شرکت نوآوران تأمین",
        contact_person="مهندس رضایی",
        email="rezaei@noavaran.com",
        phone="021-98765432",
        delivery_time=7
    )
    print(f"✅ تأمین‌کننده اضافه شد:")
    print(f"نام: {new_provider.name}")
    print(f"تماس: {new_provider.contact_person} | ایمیل: {new_provider.email}")
    print(f"تلفن: {new_provider.phone} | زمان تحویل: {new_provider.delivery_time} روز")
