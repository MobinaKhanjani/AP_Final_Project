# app/routers/items.py

from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db import get_session
from app.models.item import Item
from app.schemas.item import ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "/alphabetical",
    response_model=List[ItemRead],
    summary="List all items sorted alphabetically by name",
)
def list_items_alphabetical(
    session: Session = Depends(get_session),
):
    """
    Fetches all active items, ordered by their `name` in ascending (A→Z).
    """
    statement = select(Item).where(Item.is_active == True).order_by(Item.name)
    items = session.exec(statement).all()
    return items
