from fastapi import APIRouter
from .create import router as create_router
from .update_status import router as update_status_router
from .list import router as list_router
from .get import router as get_router

router = APIRouter(tags=["Supplier Orders"])

# شامل کردن همه روترها با prefixهای متفاوت
router.include_router(create_router, tags=["Supplier Orders"])
router.include_router(update_status_router, tags=["Supplier Orders"])
router.include_router(list_router,  tags=["Supplier Orders"])
router.include_router(get_router,  tags=["Supplier Orders"])