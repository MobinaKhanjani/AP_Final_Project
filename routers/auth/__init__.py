from fastapi import APIRouter
from .register import router as register_router
from .login import router as login_router
from .me_get import router as me_get_router
from .me_put import router as me_put_router

router = APIRouter(tags=["Authentication"])

router.include_router(register_router)
router.include_router(login_router)
router.include_router(me_get_router)
router.include_router(me_put_router)