from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Models.item import ItemCreate, Item
from database import get_session

router = APIRouter()

@router.post("/items", response_model=Item)
def create_item(item_data: ItemCreate, session: Session = Depends(get_session)):
    item = Item.from_orm(item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
