from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from database import get_session
from Models.user import User
from security import create_access_token

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), #+
    session: Session = Depends(get_session)
):
    """
    ورود کاربر و دریافت توکن
    """
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="حساب کاربری غیرفعال است"
        )
    
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }