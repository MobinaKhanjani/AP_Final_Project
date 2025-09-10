from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_session
from Models import Item, ItemRead
from sqlmodel import select
from typing import List

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/sortedbyprice", response_model=List[ItemRead])
def get_items_sorted_by_price(db: Session = Depends(get_session)):
    try:
        statement = select(Item).order_by(Item.price)
        items = db.exec(statement).all()
        return items
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"خطا در دریافت آیتم‌ها: {str(e)}"}
        )