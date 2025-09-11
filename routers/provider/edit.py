from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Models.Provider import Provider, ProviderUpdate
from database import get_session
from security import get_current_user
from Models.user import User
router = APIRouter()

@router.put("/edit/{provider_id}", response_model=Provider)
def update_provider(provider_id: int, update_data: ProviderUpdate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    provider = session.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="تأمین‌کننده پیدا نشد")

    update_fields = update_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(provider, key, value)

    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider
