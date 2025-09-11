from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from database import get_session
from Models.customer_order import CustomerOrder, CustomerOrderCreate, CustomerOrderRead, CustomerOrderStatus
from Models.customer_order import CustomerOrderItem
from Models.item import Item
from Models.user import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# مدل برای آیتم‌های سفارش
class OrderItemRequest(BaseModel):
    item_id: int
    quantity: int

# مدل برای درخواست ایجاد سفارش
class CustomerOrderCreateRequest(BaseModel):
    user_id: int
    items: List[OrderItemRequest]
    status: CustomerOrderStatus = CustomerOrderStatus.DRAFT

# مدل برای پاسخ سفارش
class CustomerOrderResponse(BaseModel):
    id: int  # Order ID
    user_id: int
    status: CustomerOrderStatus
    created_at: str
    total_price: float
    items: List[dict]
    message: str = "سفارش با موفقیت ثبت شد"

@router.post("/", response_model=CustomerOrderResponse)
def create_customer_order(
    order_data: CustomerOrderCreateRequest, 
    session: Session = Depends(get_session)
):
    """
    ایجاد سفارش جدید با قابلیت ثبت چندین کالا
    - بررسی موجودی کالاها
    - کاهش موجودی انبار
    - محاسبه قیمت کل
    - بازگرداندن Order ID
    """
    
    # بررسی وجود کاربر
    user = session.get(User, order_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="کاربر یافت نشد"
        )
    
    # بررسی موجودی و محاسبه قیمت کل
    total_price = 0.0
    order_items = []
    items_details = []
    
    for item_request in order_data.items:
        # پیدا کردن کالا
        item = session.get(Item, item_request.item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"کالا با شناسه {item_request.item_id} یافت نشد"
            )
        
        # بررسی موجودی کافی
        if item.quantity < item_request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"موجودی کافی برای کالا '{item.name}' نیست. موجودی: {item.quantity}"
            )
        
        # کاهش موجودی
        item.quantity -= item_request.quantity
        
        # محاسبه قیمت
        item_total = item.price * item_request.quantity
        total_price += item_total
        
        # ایجاد آیتم سفارش
        order_item = CustomerOrderItem(
            item_id=item_request.item_id,
            quantity=item_request.quantity
        )
        order_items.append(order_item)
        
        # اطلاعات آیتم برای پاسخ
        items_details.append({
            "item_id": item.id,
            "name": item.name,
            "sku": item.sku,
            "quantity": item_request.quantity,
            "unit_price": item.price,
            "item_total": item_total
        })
    
    # ایجاد سفارش
    order = CustomerOrder(
        user_id=order_data.user_id,
        status=order_data.status,
        items=order_items
    )
    
    session.add(order)
    session.commit()
    session.refresh(order)
    
    # ایجاد پاسخ با Order ID
    response = CustomerOrderResponse(
        id=order.id,  # Order ID
        user_id=order.user_id,
        status=order.status,
        created_at=order.created_at.isoformat(),
        total_price=total_price,
        items=items_details,
        message=f"سفارش با شماره {order.id} با موفقیت ثبت شد"
    )
    
    return response