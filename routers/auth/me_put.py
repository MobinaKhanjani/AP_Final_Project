from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from security import get_current_user
from Models.user import User, UserRead, UserUpdate

router = APIRouter()

@router.put("/me", response_model=UserRead)
async def update_current_user(
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    بروزرسانی اطلاعات کاربر جاری
    """
    user_data = user_update.dict(exclude_unset=True)
    
    if "password" in user_data:
        user_data["hashed_password"] = User.get_password_hash(user_data.pop("password"))
    
    for key, value in user_data.items():
        setattr(current_user, key, value)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return current_user