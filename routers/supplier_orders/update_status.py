from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel, select
from database import get_session
from security import get_current_user
from Models.user import User
from Models.supplier_order import SupplierOrder, SupplierOrderStatus, SupplierOrderItem
from Models.item import Item

router = APIRouter()

class StatusUpdateRequest(SQLModel):
    status: SupplierOrderStatus

@router.put("/supplier-orders/{order_id}/status", response_model=SupplierOrder)
async def update_supplier_order_status(
    order_id: int,
    status_data: StatusUpdateRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    تغییر وضعیت سفارش و افزایش خودکار موجودی انبار هنگام رسیدن کالا
    """
    # پیدا کردن سفارش
    order = session.get(SupplierOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="سفارش یافت نشد")
    
    # ذخیره وضعیت قبلی برای بررسی تغییرات
    old_status = order.status
    new_status = status_data.status
    
    # بروزرسانی وضعیت
    order.status = new_status
    order.notes = f"{order.notes or ''}\nتغییر وضعیت از {old_status} به {new_status} توسط {current_user.username}".strip()
    
    # اگر وضعیت به RECEIVED تغییر کرد: افزایش موجودی انبار
    if old_status != SupplierOrderStatus.RECEIVED and new_status == SupplierOrderStatus.RECEIVED:
        await _increase_inventory(order_id, session, current_user)
    
    session.add(order)
    session.commit()
    session.refresh(order)
    
    return order

async def _increase_inventory(order_id: int, session: Session, current_user: User):
    """
    افزایش خودکار موجودی انبار پس از دریافت کالا
    """
    # پیدا کردن تمام آیتم‌های سفارش
    order_items = session.exec(
        select(SupplierOrderItem)
        .where(SupplierOrderItem.order_id == order_id)
    ).all()
    
    for order_item in order_items:
        item = session.get(Item, order_item.item_id)
        if item:
            # افزایش موجودی
            item.quantity += order_item.quantity
            item.notes = f"{item.notes or ''}\nافزایش موجودی: +{order_item.quantity} via سفارش #{order_id} توسط {current_user.username}".strip()
            
            session.add(item)
    
    session.commit()
    
    #تغییر وضعیت سفارش بین مراحل مختلف

#ثبت تاریخچه تغییرات در notes

#افزایش خودکار موجودی انبار وقتی وضعیت به received می‌رسه

#بررسی منطقی تغییر وضعیت (پرش از مراحل مجاز نیست)