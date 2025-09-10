from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select  
from database import get_session
from Models.Provider import Provider
from Models.item import Item  # برای بررسی وابستگی

router = APIRouter()

@router.delete("/delete/{provider_id}")
def delete_provider(
    provider_id: int, 
    session: Session = Depends(get_session)  # ✅ تغییر به session
):
    # پیدا کردن تامین‌کننده
    provider = session.get(Provider, provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="تأمین‌کننده پیدا نشد"
        )
    
    # بررسی آیا محصولاتی مرتبط با این تامین‌کننده وجود دارند
    related_items = session.exec(
        select(Item).where(Item.provider_id == provider_id)
    ).all()
    
    if related_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="امکان حذف تامین‌کننده وجود ندارد زیرا محصولاتی به آن مرتبط هستند"
        )
    
    # حذف تامین‌کننده
    session.delete(provider)
    session.commit()
    
    return {"message": "تأمین‌کننده با موفقیت حذف شد"}