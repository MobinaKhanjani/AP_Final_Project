from fastapi import APIRouter
from .low_stock import router as low_stock_router
from .rate_delivery import router as rate_delivery_router
from .top_selling import router as top_selling_router

router = APIRouter(tags=["Reports"])

# شامل کردن همه روترهای گزارشات
router.include_router(low_stock_router)
router.include_router(rate_delivery_router)
router.include_router(top_selling_router)

# router.include_router(low_stock_router, prefix="/reports")
# router.include_router(rate_delivery_router, prefix="/reports")
# router.include_router(top_selling_router, prefix="/reports")