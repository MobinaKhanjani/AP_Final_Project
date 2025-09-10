from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_session
from Models import Item, ItemRead

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/search/sku/{sku}", response_model=ItemRead)
def get_item_by_sku(sku: str, db: Session = Depends(get_session)):
    try:
        item = db.query(Item).filter(Item.sku == sku).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"آیتم با کد SKU '{sku}' پیدا نشد"
            )
        return item
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"خطا در دریافت آیتم: {str(e)}"}
        )
