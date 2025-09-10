from fastapi import APIRouter, Depends, HTTPException
from Models.customer_order import CustomerOrderCreate, CustomerOrder, CustomerOrderItem
from database import get_session
from sqlmodel import Session

router = APIRouter()

@router.post("/customer-orders", response_model=CustomerOrder)
def create_order(order_data: CustomerOrderCreate, session: Session = Depends(get_session)):
    order = CustomerOrder(user_id=order_data.user_id)
    session.add(order)
    session.commit()
    session.refresh(order)

    for item in order_data.items:
        order_item = CustomerOrderItem(order_id=order.id, item_id=item.item_id, quantity=item.quantity)
        session.add(order_item)

    session.commit()
    return order
#ثبت سفارش