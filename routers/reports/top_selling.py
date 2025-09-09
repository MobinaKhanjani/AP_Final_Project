from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta
from database import get_session
from security import get_current_user
from Models.user import User
from Models.order import Order, OrderItem, OrderStatus
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
                func.sum(OrderItem.quantity).label("total_sold"),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label("total_revenue"),
                func.count(OrderItem.order_id).label("order_count")
            )
            .join(OrderItem, OrderItem.item_id == Item.id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(
                Order.created_at >= start_time,
                Order.status.in_([OrderStatus.RECEIVED, OrderStatus.CLOSED]),  # فقط سفارشات تکمیل شده
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

# @router.get("/top-selling/daily", response_model=List[Dict[str, Any]])
# async def get_daily_top_selling_items(
#     days: int = Query(7, ge=1, le=30, description="تعداد روزهای گذشته"),
#     limit: int = Query(10, ge=1, le=100, description="تعداد آیتم‌های بازگشتی"),
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user)
# ):
#     """
#     دریافت پرفروش‌ترین کالاها در روزهای اخیر (گروه‌بندی روزانه)
#     """
#     try:
#         start_time = datetime.utcnow() - timedelta(days=days)
        
#         daily_top_query = (
#             select(
#                 Item.id,
#                 Item.name,
#                 Item.sku,
#                 func.date(Order.created_at).label("sale_date"),
#                 func.sum(OrderItem.quantity).label("daily_sold"),
#                 func.sum(OrderItem.quantity * OrderItem.unit_price).label("daily_revenue")
#             )
#             .join(OrderItem, OrderItem.item_id == Item.id)
#             .join(Order, Order.id == OrderItem.order_id)
#             .where(
#                 Order.created_at >= start_time,
#                 Order.status.in_([OrderStatus.RECEIVED, OrderStatus.CLOSED]),
#                 Item.is_active == True
#             )
#             .group_by(Item.id, Item.name, Item.sku, func.date(Order.created_at))
#             .order_by(desc("daily_sold"))
#             .limit(limit)
#         )
        
#         results = session.exec(daily_top_query).all()
        
#         daily_items = []
#         for result in results:
#             item_id, name, sku, sale_date, daily_sold, daily_revenue = result
            
#             daily_items.append({
#                 "id": item_id,
#                 "name": name,
#                 "sku": sku,
#                 "sale_date": sale_date,
#                 "daily_sold": daily_sold,
#                 "daily_revenue": daily_revenue,
#                 "days_ago": (datetime.utcnow().date() - sale_date).days
#             })
        
#         return daily_items
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"خطا در دریافت آمار روزانه: {str(e)}"
#         )