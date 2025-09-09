from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from datetime import datetime
from typing import Dict, Any
from database import get_session
from security import get_current_user
from Models.user import User
from Models.Provider import Provider
from Models.supplier_order import SupplierOrder, SupplierOrderStatus

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
    ثبت امتیاز تحویل برای تامین‌کننده بر اساس سرعت و صحت تحویل
    """
    # بررسی وجود تامین‌کننده
    provider = session.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="تامین‌کننده یافت نشد")
    
    # بررسی وجود سفارش
    order = session.get(SupplierOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="سفارش یافت نشد")
    
    # بررسی ارتباط سفارش با تامین‌کننده
    if order.provider_id != provider_id:
        raise HTTPException(status_code=400, detail="سفارش مربوط به این تامین‌کننده نیست")
    
    # بررسی وضعیت سفارش
    if order.status != SupplierOrderStatus.RECEIVED:
        raise HTTPException(
            status_code=400, 
            detail="فقط سفارشات دریافت شده قابل امتیازدهی هستند"
        )
    
    # ثبت امتیازات
    provider.delivery_time_rating = time_rating
    provider.delivery_accuracy_score = accuracy_score
    
    session.add(provider)
    session.commit()
    session.refresh(provider)
    
    return {
        "message": "امتیاز با موفقیت ثبت شد",
        "provider_id": provider.id,
        "provider_name": provider.name,
        "time_rating": time_rating,
        "accuracy_score": accuracy_score,
        "rated_at": datetime.utcnow()
    }