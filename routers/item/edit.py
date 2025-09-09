from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.item import Item, ItemUpdate
from database import get_session

router = APIRouter()

@router.put("/items/edit/{item_id}", response_model=Item)
def edit_item(item_id: int, item_update: ItemUpdate, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="آیتم پیدا نشد")

    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item
