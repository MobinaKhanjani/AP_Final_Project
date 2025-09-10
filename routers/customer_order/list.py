from fastapi import APIRouter, Depends
from sqlmodel import select
from app.models.customer_order import CustomerOrder, CustomerOrderStatus
from app.database import get_session
from typing import List, Optional

router = APIRouter()

@router.get("/customer-orders", response_model=List[CustomerOrder])
def list_orders(
    status: Optional[CustomerOrderStatus] = None,
    page: int = 1,
    limit: int = 10,
    session=Depends(get_session)
):
    query = select(CustomerOrder)
    if status:
        query = query.where(CustomerOrder.status == status)
    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()
