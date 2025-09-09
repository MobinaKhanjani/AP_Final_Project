from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models.order import Order
from app.schemas.order import OrderRead

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get(
    "/",
    response_model=List[OrderRead],
    status_code=status.HTTP_200_OK,
)
def get_all_orders(session: Session = Depends(get_session)):
    """
    دریافت لیست کامل سفارش‌ها
    """
    statement = select(Order)
    orders = session.exec(statement).all()
    return orders