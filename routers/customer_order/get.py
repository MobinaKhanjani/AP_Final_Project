from fastapi import APIRouter, Depends, HTTPException
from app.models.customer_order import CustomerOrder, CustomerOrderRead
from app.database import get_session

router = APIRouter()

@router.get("/customer-orders/{order_id}", response_model=CustomerOrderRead)
def get_order(order_id: int, session=Depends(get_session)):
    order = session.get(CustomerOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="سفارش پیدا نشد")
    return order
#دریافت جزئیات سفارش