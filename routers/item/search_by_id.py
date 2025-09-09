from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_session
from Models.item import Item, ItemRead

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/search/{item_id}", response_model=ItemRead)
def get_item_by_id(item_id: int, db: Session = Depends(get_session)):
    try:
        item = db.get(Item, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"آیتم با شناسه {item_id} پیدا نشد"
            )
        return item
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"خطا در دریافت آیتم: {str(e)}"}
        )