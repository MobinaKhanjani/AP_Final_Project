from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from database import get_session
from Models.customer_order import CustomerOrder, CustomerOrderStatus
from Models.customer_order import CustomerOrderItem
from Models.item import Item
from Models.user import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# مدل برای آیتم‌های سفارش در پاسخ
class OrderItemResponse(BaseModel):
    id: int
    item_id: int
    item_name: str
    item_sku: str
    quantity: int
    unit_price: float
    item_total: float

# مدل برای پاسخ لیست سفارشات
class CustomerOrderListResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    status: CustomerOrderStatus
    created_at: datetime
    total_price: float
    item_count: int
    items: List[OrderItemResponse]

# مدل برای پارامترهای جستجو
class OrderFilterParams(BaseModel):
    user_id: Optional[int] = None
    status: Optional[CustomerOrderStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 100

@router.get("/", response_model=List[CustomerOrderListResponse])
def get_customer_orders(
    user_id: Optional[int] = None,
    status: Optional[CustomerOrderStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    دریافت لیست سفارشات مشتریان با قابلیت فیلتر کردن
    - فیلتر بر اساس کاربر
    - فیلتر بر اساس وضعیت سفارش
    - فیلتر بر اساس تاریخ
    """
    
    # ساخت کوئری پایه
    query = select(CustomerOrder)
    
    # اعمال فیلترها
    if user_id:
        query = query.where(CustomerOrder.user_id == user_id)
    
    if status:
        query = query.where(CustomerOrder.status == status)
    
    if start_date:
        query = query.where(CustomerOrder.created_at >= start_date)
    
    if end_date:
        query = query.where(CustomerOrder.created_at <= end_date)
    
    # مرتب سازی بر اساس تاریخ ایجاد (جدیدترین اول)
    query = query.order_by(CustomerOrder.created_at.desc())
    
    # اعمال pagination
    query = query.offset(skip).limit(limit)
    
    # اجرای کوئری
    orders = session.exec(query).all()
    
    # پردازش سفارشات و محاسبه قیمت کل
    orders_response = []
    
    for order in orders:
        total_price = 0.0
        item_count = 0
        items_details = []
        
        # محاسبه قیمت کل و جزئیات آیتم‌ها
        for order_item in order.items:
            item = session.get(Item, order_item.item_id)
            if item:
                item_total = item.price * order_item.quantity
                total_price += item_total
                item_count += 1
                
                items_details.append(OrderItemResponse(
                    id=order_item.id,
                    item_id=item.id,
                    item_name=item.name,
                    item_sku=item.sku,
                    quantity=order_item.quantity,
                    unit_price=item.price,
                    item_total=item_total
                ))
        
        # اطلاعات کاربر
        user = session.get(User, order.user_id)
        user_name = user.full_name if user and user.full_name else user.username if user else "نامشخص"
        
        # ایجاد پاسخ
        order_response = CustomerOrderListResponse(
            id=order.id,
            user_id=order.user_id,
            user_name=user_name,
            status=order.status,
            created_at=order.created_at,
            total_price=total_price,
            item_count=item_count,
            items=items_details
        )
        
        orders_response.append(order_response)
    
    return orders_response

@router.get("/{order_id}", response_model=CustomerOrderListResponse)
def get_customer_order_by_id(
    order_id: int,
    session: Session = Depends(get_session)
):
    """
    دریافت اطلاعات کامل یک سفارش بر اساس ID
    """
    
    order = session.get(CustomerOrder, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="سفارش یافت نشد"
        )
    
    total_price = 0.0
    item_count = 0
    items_details = []
    
    # محاسبه قیمت کل و جزئیات آیتم‌ها
    for order_item in order.items:
        item = session.get(Item, order_item.item_id)
        if item:
            item_total = item.price * order_item.quantity
            total_price += item_total
            item_count += 1
            
            items_details.append(OrderItemResponse(
                id=order_item.id,
                item_id=item.id,
                item_name=item.name,
                item_sku=item.sku,
                quantity=order_item.quantity,
                unit_price=item.price,
                item_total=item_total
            ))
    
    # اطلاعات کاربر
    user = session.get(User, order.user_id)
    user_name = user.full_name if user and user.full_name else user.username if user else "نامشخص"
    
    return CustomerOrderListResponse(
        id=order.id,
        user_id=order.user_id,
        user_name=user_name,
        status=order.status,
        created_at=order.created_at,
        total_price=total_price,
        item_count=item_count,
        items=items_details
    )