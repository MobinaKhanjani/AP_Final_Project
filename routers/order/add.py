# app/routers/orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.db import get_session
from app.models.order import Order, OrderItem
from app.models.item import Item
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.order import OrderItemCreate   # assume you’ve defined this

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    payload: OrderCreate,
    session: Session = Depends(get_session),
):
    """
    Create a new order along with its line items.
    - Validates stock
    - Deducts inventory
    - Calculates total_price
    """

    # 1) Must have at least one item
    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must include at least one item.",
        )

    # 2) Create the Order row (in DRAFT state by default)
    db_order = Order(
        user_id=payload.user_id,
        notes=payload.notes,
        status=payload.status,
        total_price=0,  # will update after processing items
    )
    session.add(db_order)
    session.flush()   # assign db_order.id before inserting OrderItems

    total = 0.0

    # 3) Process each line item
    for line in payload.items:  # OrderItemCreate with item_id & quantity
        db_item = session.get(Item, line.item_id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id={line.item_id} not found.",
            )

        if db_item.quantity < line.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for '{db_item.name}'.",
            )

        # compute pricing
        unit_price = db_item.price
        line_total = unit_price * line.quantity

        # create pivot row
        order_item = OrderItem(
            order_id=db_order.id,
            item_id=db_item.id,
            quantity=line.quantity,
            unit_price=unit_price,
            total_price=line_total,
        )
        session.add(order_item)

        # deduct inventory
        db_item.quantity -= line.quantity
        session.add(db_item)

        total += line_total

    # 4) Update the order total and commit everything
    db_order.total_price = total
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order
