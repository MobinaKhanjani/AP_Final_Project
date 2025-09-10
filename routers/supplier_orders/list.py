from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from database import get_session
from security import get_current_user
#from Models.user import User
from Models.supplier_order import SupplierOrder, SupplierOrderStatus


router = APIRouter()

@router.get("/supplier-orders", response_model=List[SupplierOrder])
async def list_supplier_orders(
    status: Optional[SupplierOrderStatus] = Query(None, description="فیلتر بر اساس وضعیت"),
    provider_id: Optional[int] = Query(None, description="فیلتر بر اساس تامین‌کننده"),
    skip: int = Query(0, ge=0, description="تعداد رکوردهای رد شده"),
    limit: int = Query(100, ge=1, le=1000, description="تعداد رکوردهای بازگشتی"),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)  # ✅ حذف type annotation
):
    """
    مشاهده لیست سفارشات خرید از تامین‌کنندگان
    با امکان فیلتر بر اساس وضعیت و تامین‌کننده
    """
    # ساخت کوئری پایه
    query = select(SupplierOrder)
    
    # اعمال فیلترها
    if status:
        query = query.where(SupplierOrder.status == status)
    
    if provider_id:
        query = query.where(SupplierOrder.provider_id == provider_id)
    
    # مرتب‌سازی بر اساس تاریخ ایجاد (جدیدترین اول)
    query = query.order_by(SupplierOrder.created_at.desc())
    
    # صفحه‌بندی
    query = query.offset(skip).limit(limit)
    
    # اجرای کوئری
    orders = session.exec(query).all()
    
    return orders
#لیست کامل سفارشات از تامین‌کنندگان

#فیلتر بر اساس وضعیت (draft, sent, received, closed)

#فیلتر بر اساس تامین‌کننده خاص

#صفحه‌بندی برای مدیریت داده‌های زیاد

#مرتب‌سازی بر اساس تاریخ ایجاد (جدیدترین اول)