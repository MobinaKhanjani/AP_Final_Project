from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_session
from Models.provider import Provider

router = APIRouter(prefix="/provider", tags=["provider"])

@router.delete("/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_session)):
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="تأمین‌کننده پیدا نشد"
        )
    db.delete(provider)
    db.commit()
    return {"message": "تأمین‌کننده با موفقیت حذف شد"}