from fastapi import APIRouter
from .add import router as add_router
from .edit import router as edit_router
from .delete import router as delete_router

router = APIRouter(tags=["Providers"])

# شامل کردن روترها
router.include_router(add_router)
router.include_router(edit_router)
router.include_router(delete_router)