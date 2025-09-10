from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from Models.item import Item
from database import get_session

router = APIRouter()

@router.get("/items/search/sku", response_model=Item)
def search_item_by_sku(sku: str, session=Depends(get_session)):
    query = select(Item).where(Item.sku == sku)
    item = session.exec(query).first()
    if not item:
        raise HTTPException(status_code=404, detail="کالا با این SKU پیدا نشد")
    return item
