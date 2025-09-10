from fastapi import APIRouter, Depends
from sqlmodel import select
from app.models.item import Item
from app.database import get_session
from typing import List

router = APIRouter()

@router.get("/items/search/name", response_model=List[Item])
def search_items_by_name(name: str, session=Depends(get_session)):
    query = select(Item).where(Item.name.contains(name))
    return session.exec(query).all()
