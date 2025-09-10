from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_session
from ...models import ItemRead, Item
from sqlmodel import select

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/sorted-by-name", response_model=List[ItemRead])
def get_items_sorted_by_name(db: Session = Depends(get_session)):
    try:
        statement = select(Item).order_by(Item.name)
        items = db.exec(statement).all()
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت آیتم‌ها: {str(e)}"
        )