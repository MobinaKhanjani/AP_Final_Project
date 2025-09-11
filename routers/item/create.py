from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Models.item import ItemCreate, Item
from database import get_session
from security import get_current_user
from Models.user import User

router = APIRouter()

@router.post("/Create", response_model=Item)
def create_item(item_data: ItemCreate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    item = Item.from_orm(item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
