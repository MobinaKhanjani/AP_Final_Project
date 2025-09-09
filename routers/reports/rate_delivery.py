from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session 
from datetime import datetime
from typing import Dict, Any
from database import get_session
from security import get_current_user
from Models.user import User
from Models.Provider import Provider
from Models.order import Order, OrderStatus

router = APIRouter()

@router.post("/providers/{provider_id}/rate-delivery", response_model=Dict[str, Any])
async def rate_provider_delivery(
    provider_id: int,
    time_rating: int = Query(..., ge=1, le=5, description="امتیاز سرعت تحویل (1-5)"),
    accuracy_score: int = Query(..., ge=0, le=100, description="امتیاز صحت تحویل (0-100)"),
    order_id: int = Query(..., description="ID سفارش مربوطه"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    ثبت امتیاز تحویل برای تامین‌کننده بر اساس یک سفارش خاص
    """
    try:
        # بررسی وجود تامین‌کننده
        provider = session.get(Provider, provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="تامین‌کننده یافت نشد")
        
        # بررسی وجود سفارش و ارتباط با تامین‌کننده
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="سفارش یافت نشد")
        
        if order.provider_id != provider_id:
            raise HTTPException(status_code=400, detail="سفارش مربوط به این تامین‌کننده نیست")
        
        # بررسی وضعیت سفارش (فقط سفارشات تحویل شده قابل امتیازدهی هستند)
        if order.status != OrderStatus.RECEIVED and order.status != OrderStatus.CLOSED:
            raise HTTPException(
                status_code=400, 
                detail="فقط سفارشات تحویل شده قابل امتیازدهی هستند"
            )
        
        # بروزرسانی امتیازات تامین‌کننده
        provider.delivery_time_rating = time_rating
        provider.delivery_accuracy_score = accuracy_score
        
        # همچنین می‌تونیم امتیاز رو در سفارش هم ذخیره کنیم
        # اگر فیلدهای delivery_rating و delivery_notes در Order مدل وجود دارن:
        if hasattr(order, 'delivery_rating'):
            order.delivery_rating = time_rating
        if hasattr(order, 'delivery_notes'):
            order.delivery_notes = f"امتیاز سرعت: {time_rating}, امتیاز صحت: {accuracy_score}"
        
        session.add(provider)
        session.add(order)
        session.commit()
        session.refresh(provider)
        session.refresh(order)
        
        return {
            "message": "امتیاز با موفقیت ثبت شد",
            "provider_id": provider.id,
            "provider_name": provider.name,
            "order_id": order.id,
            "time_rating": provider.delivery_time_rating,
            "accuracy_score": provider.delivery_accuracy_score,
            "rated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"خطا در ثبت امتیاز: {str(e)}"
        )

# @router.get("/providers/{provider_id}/rating", response_model=Dict[str, Any])
# async def get_provider_rating(
#     provider_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user)
# ):
#     """
#     دریافت امتیاز فعلی تامین‌کننده
#     """
#     provider = session.get(Provider, provider_id)
#     if not provider:
#         raise HTTPException(status_code=404, detail="تامین‌کننده یافت نشد")
    
#     return {
#         "provider_id": provider.id,
#         "provider_name": provider.name,
#         "delivery_time_rating": provider.delivery_time_rating,
#         "delivery_accuracy_score": provider.delivery_accuracy_score,
#         "last_updated": provider.updated_at if hasattr(provider, 'updated_at') else None
#     }