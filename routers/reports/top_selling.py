from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta
from database import get_session
from security import get_current_user
from Models.user import User
from Models.customer_order import CustomerOrder, CustomerOrderItem, CustomerOrderStatus
from Models.item import Item

router = APIRouter()

@router.get("/top-selling", response_model=List[Dict[str, Any]])
async def get_top_selling_items(
    hours: int = Query(24, ge=1, le=720, description="بازه زمانی به ساعت (1 تا 720 ساعت)"),
    limit: int = Query(10, ge=1, le=100, description="تعداد آیتم‌های بازگشتی"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت پرفروش‌ترین کالاها در بازه زمانی مشخص (پیش‌فرض: 24 ساعت اخیر)
    """
    try:
        # محاسبه تاریخ شروع بر اساس ساعت‌های requested
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        # کوئری برای پیدا کردن پرفروش‌ترین آیتم‌ها
        top_selling_query = (
            select(
                Item.id,
                Item.name,
                Item.sku,
                func.sum(CustomerOrderItem.quantity).label("total_sold"),
                func.sum(CustomerOrderItem.quantity * CustomerOrderItem.unit_price).label("total_revenue"),
                func.count(CustomerOrderItem.order_id).label("order_count")
            )
            .join(CustomerOrderItem, CustomerOrderItem.item_id == Item.id)
            .join(CustomerOrder, CustomerOrder.id == CustomerOrderItem.order_id)
            .where(
                CustomerOrder.created_at >= start_time,
                CustomerOrder.status.in_([CustomerOrderStatus.DELIVERED]),  # فقط سفارشات تحویل شده
                Item.is_active == True
            )
            .group_by(Item.id, Item.name, Item.sku)
            .order_by(desc("total_sold"))
            .limit(limit)
        )
        
        results = session.exec(top_selling_query).all()
        
        # تبدیل نتایج به فرمت مناسب
        top_items = []
        for result in results:
            item_id, name, sku, total_sold, total_revenue, order_count = result
            
            top_items.append({
                "id": item_id,
                "name": name,
                "sku": sku,
                "total_sold": total_sold,
                "total_revenue": total_revenue,
                "order_count": order_count,
                "average_order_value": total_revenue / order_count if order_count > 0 else 0,
                "time_period_hours": hours
            })
        
        return top_items
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"خطا در دریافت پرفروش‌ترین کالاها: {str(e)}"
        )