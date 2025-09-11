from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Models.item import Item
from database import get_session
from security import get_current_user
from Models.user import User


router = APIRouter()

@router.delete("/Delete/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="آیتم پیدا نشد")

    session.delete(item)
    session.commit()
    return {"detail": "آیتم با موفقیت حذف شد"}
