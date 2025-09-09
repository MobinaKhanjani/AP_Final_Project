from fastapi import APIRouter, Depends
from sqlmodel import Session
from models.item import Item, ItemCreate
from database import get_session

router = APIRouter()

@router.post("/items/add", response_model=Item)
def add_item(item: ItemCreate, session: Session = Depends(get_session)):
    new_item = Item.from_orm(item)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item
