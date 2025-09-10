from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_session
from Models.Provider import Provider, ProviderCreate

router = APIRouter(prefix="/add", tags=["provider"])

@router.post("/", response_model=ProviderCreate)
def add_provider(data: ProviderCreate, db: Session = Depends(get_session)):
    try:
        provider = Provider(**data.dict())
        db.add(provider)
        db.commit()
        db.refresh(provider)
        return provider
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در افزودن تأمین‌کننده: {str(e)}"
        )
