from fastapi import APIRouter, Depends
from sqlmodel import select
from Models.item import Item
from database import get_session
from typing import List

router = APIRouter()

@router.get("/Sort_by_price", response_model=List[Item])
def sort_items_by_price(order: str = "asc", session=Depends(get_session)):
    query = select(Item)
    if order == "desc":
        query = query.order_by(Item.price.desc())
    else:
        query = query.order_by(Item.price)
    return session.exec(query).all()
