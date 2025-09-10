from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session ,select 
from database import get_session
from Models.Provider import Provider, ProviderCreate, ProviderRead

router = APIRouter()

@router.post("/", response_model=ProviderRead)
def add_provider(
    data: ProviderCreate, 
    session: Session = Depends(get_session)  
):
    try:
        # بررسی وجود تامین‌کننده با همین نام
        existing_provider = session.exec(
            select(Provider).where(Provider.name == data.name)
        ).first()
        
        if existing_provider:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="تامین‌کننده با این نام قبلاً ثبت شده است"
            )
        
        provider = Provider.from_orm(data)
        session.add(provider)
        session.commit()
        session.refresh(provider)
        return provider
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در افزودن تأمین‌کننده: {str(e)}"
        )