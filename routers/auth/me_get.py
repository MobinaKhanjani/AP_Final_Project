from fastapi import APIRouter, Depends
from security import get_current_user
from Models.user import User, UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """
    دریافت اطلاعات کاربر جاری
    """
    return current_user