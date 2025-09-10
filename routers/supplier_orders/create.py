from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel
from typing import List
from database import get_session
from security import get_current_user
from Models.user import User
from Models.Provider import Provider
from Models.item import Item
from Models.supplier_order import SupplierOrder, SupplierOrderStatus, SupplierOrderItem

router = APIRouter()

class SupplierOrderCreateRequest(SQLModel):
    provider_id: int
    items: List[dict]  # [{"item_id": 1, "quantity": 10}, ...]

@router.post("/supplier-orders", response_model=SupplierOrder)
async def create_supplier_order(
    order_data: SupplierOrderCreateRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    ثبت سفارش خرید جدید از تامین‌کننده
    شامل: لیست کالاها، تعداد و تامین‌کننده مربوطه
    """
    # بررسی وجود تامین‌کننده
    provider = session.get(Provider, order_data.provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="تامین‌کننده یافت نشد")
    
    # ایجاد سفارش جدید
    new_order = SupplierOrder(
        provider_id=order_data.provider_id,
        status=SupplierOrderStatus.DRAFT,
        notes=f"سفارش ایجاد شده توسط کاربر: {current_user.username}"
    )
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    
    # افزودن آیتم‌های سفارش
    total_price = 0
    for item_data in order_data.items:
        item = session.get(Item, item_data["item_id"])
        if not item:
            continue  # یا خطا بدهید
            
        order_item = SupplierOrderItem(
            order_id=new_order.id,
            item_id=item.id,
            quantity=item_data["quantity"],
            unit_price=item.price,
            total_price=item.price * item_data["quantity"]
        )
        
        total_price += order_item.total_price
        session.add(order_item)
    
    # بروزرسانی قیمت کل سفارش
    new_order.total_price = total_price
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    
    return new_order

#ثبت سفارش جدید با وضعیت DRAFT

#بررسی وجود تامین‌کننده

#محاسبه خودکار قیمت بر اساس قیمت محصولات

#ثبت تمام آیتم‌های سفارش

#برگشت اطلاعات کامل سفارش ایجاد شده