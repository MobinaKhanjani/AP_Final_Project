from fastapi import APIRouter, Depends, HTTPException , Query
from sqlmodel import Session, select
from datetime import datetime
from database import get_session
from security import get_current_user
from Models.user import User
from Models.Provider import Provider
from Models.order import Order

router = APIRouter()



@router.post("/providers/{provider_id}/rate-delivery")
async def rate_provider_delivery(
    provider_id: int,
    time_rating: int = Query(..., ge=1, le=5, description="امتیاز سرعت تحویل (1-5)"),
    accuracy_score: int = Query(..., ge=0, le=100, description="امتیاز صحت تحویل (0-100)"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    ثبت امتیاز تحویل برای تامین‌کننده
    """
    provider = session.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="تامین‌کننده یافت نشد")
    
    # بروزرسانی امتیازات
    provider.delivery_time_rating = time_rating
    provider.delivery_accuracy_score = accuracy_score
    
    session.add(provider)
    session.commit()
    session.refresh(provider)
    
    return {
        "message": "امتیاز با موفقیت ثبت شد",
        "provider_id": provider.id,
        "time_rating": provider.delivery_time_rating,
        "accuracy_score": provider.delivery_accuracy_score
    }