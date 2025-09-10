from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models.item import ItemUpdate, Item
from app.database import get_session

router = APIRouter()

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, update_data: ItemUpdate, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="آیتم پیدا نشد")

    update_fields = update_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(item, key, value)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item
