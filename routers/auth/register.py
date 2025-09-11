from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from Models.user import User, UserCreate, UserRead

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    ثبت‌نام کاربر جدید
    """
    # بررسی وجود کاربر با همین نام کاربری
    existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نام کاربری قبلاً ثبت شده است"
        )
    
    # بررسی وجود کاربر با همین ایمیل
    existing_email = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ایمیل قبلاً ثبت شده است"
        )
    
    # ایجاد کاربر جدید
    hashed_password = User.get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user