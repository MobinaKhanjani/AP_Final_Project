from fastapi import APIRouter, Depends
from sqlmodel import select
from app.models.item import Item
from app.database import get_session
from typing import List

router = APIRouter()

@router.get("/items/sort/name", response_model=List[Item])
def sort_items_by_name(order: str = "asc", session=Depends(get_session)):
    query = select(Item)
    if order == "desc":
        query = query.order_by(Item.name.desc())
    else:
        query = query.order_by(Item.name)
    return session.exec(query).all()
