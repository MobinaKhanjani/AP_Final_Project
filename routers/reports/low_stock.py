from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from typing import List, Dict, Any
from database import get_session
from security import get_current_user
from Models.user import User
from Models.item import Item

router = APIRouter()

@router.get("/low-stock", response_model=List[Dict[str, Any]])
async def get_low_stock_items(
    critical_only: bool = Query(False, description="فقط کالاهای تمام شده نمایش داده شود"),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)  
):
    
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User inactive")
    
    """
    دریافت لیست کالاهای با موجودی کم یا تمام شده
    """
    try:
        if critical_only:
            statement = select(Item).where(
                Item.quantity == 0,
                Item.is_active == True
            )
        else:
            statement = select(Item).where(
                Item.quantity <= Item.min_threshold,
                Item.is_active == True
            )
        
        low_stock_items = session.exec(statement).all()
        
        result = []
        for item in low_stock_items:
            needed_quantity = max(0, item.min_threshold - item.quantity)
            
            if item.quantity == 0:
                alert_level = "critical"
                status = "تمام شده"
            elif item.quantity <= item.min_threshold * 0.3:
                alert_level = "high"
                status = "موجودی بسیار کم"
            else:
                alert_level = "medium"
                status = "موجودی کم"
            
            result.append({
                "id": item.id,
                "name": item.name,
                "sku": item.sku,
                "current_quantity": item.quantity,
                "min_threshold": item.min_threshold,
                "needed_quantity": needed_quantity,
                "alert_level": alert_level,
                "status": status,
                "price": item.price,
                "is_out_of_stock": item.quantity == 0
            })
        
        result.sort(key=lambda x: 0 if x["alert_level"] == "critical" else 1)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در دریافت کالاهای کم موجودی: {str(e)}")