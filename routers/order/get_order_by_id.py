from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from database import get_session
from Models.order import Order, OrderItem, OrderRead
from Models.item import Item

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    "/quick",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def quick_order_by_item_id(
    item_id: Annotated[int, Depends()],
    quantity: Annotated[int, Depends()],
    user_id: Annotated[int, Depends()],
    session: Session = Depends(get_session),
):
    """
    ثبت سفارش سریع فقط با item_id و quantity و user_id
    """
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="تعداد باید بیشتر از صفر باشد.")

    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="کالا پیدا نشد.")

    if db_item.quantity < quantity:
        raise HTTPException(status_code=400, detail="موجودی کافی نیست.")

    # ساخت سفارش
    order = Order(user_id=user_id, total_price=0)
    session.add(order)
    session.flush()  # گرفتن order.id قبل از ساخت OrderItem

    # ساخت آیتم سفارش
    unit_price = db_item.price
    total_price = unit_price * quantity

    order_item = OrderItem(
        order_id=order.id,
        item_id=item_id,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
    )
    session.add(order_item)

    # کاهش موجودی کالا
    db_item.quantity -= quantity
    session.add(db_item)

    # به‌روزرسانی قیمت سفارش
    order.total_price = total_price
    session.add(order)
    session.commit()
    session.refresh(order)

    return order