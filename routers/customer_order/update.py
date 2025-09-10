from fastapi import APIRouter, Depends, HTTPException
from app.models.customer_order import CustomerOrder, CustomerOrderUpdate
from app.database import get_session

router = APIRouter()

@router.put("/customer-orders/{order_id}", response_model=CustomerOrder)
def update_order(order_id: int, update_data: CustomerOrderUpdate, session=Depends(get_session)):
    order = session.get(CustomerOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="سفارش پیدا نشد")

    if update_data.status:
        order.status = update_data.status

    session.add(order)
    session.commit()
    session.refresh(order)
    return order
#به روزرسانی وضعیت با آیتم های سفارش