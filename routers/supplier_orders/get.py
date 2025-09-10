from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from security import get_current_user

router = APIRouter()

@router.get("/supplier-orders/{order_id}", response_model=dict)
async def get_supplier_order(
    order_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)  # ✅ بدون type annotation
):
    """
    دریافت جزئیات کامل یک سفارش خاص از تامین‌کننده
    شامل اطلاعات سفارش و آیتم‌های مربوطه
    """
    from Models.supplier_order import SupplierOrder, SupplierOrderItem
    from Models.Provider import Provider
    from Models.item import Item
    
    # پیدا کردن سفارش
    order = session.get(SupplierOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="سفارش یافت نشد")
    
    # پیدا کردن آیتم‌های سفارش
    order_items = session.exec(
        select(SupplierOrderItem)
        .where(SupplierOrderItem.order_id == order_id)
    ).all()
    
    # پیدا کردن اطلاعات تامین‌کننده
    provider = session.get(Provider, order.provider_id)
    
    # آماده کردن response
    order_data = order.dict()
    
    # اضافه کردن آیتم‌های سفارش با اطلاعات کامل
    items_with_details = []
    for item in order_items:
        item_data = item.dict()
        item_details = session.get(Item, item.item_id)
        if item_details:
            item_data["item_name"] = item_details.name
            item_data["item_sku"] = item_details.sku
        items_with_details.append(item_data)
    
    order_data["items"] = items_with_details
    order_data["provider_name"] = provider.name if provider else "نامشخص"
    
    return order_data