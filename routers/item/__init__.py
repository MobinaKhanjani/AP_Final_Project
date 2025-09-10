from fastapi import APIRouter

from .create import router as create_router
from .update import router as update_router
from .delete import router as delete_router

from .search_by_name import router as search_name_router
from .search_by_sku import router as search_sku_router
from .sort_by_price import router as sort_price_router
from .sort_by_alphbet import router as sort_name_router

router = APIRouter()
router.include_router(create_router, tags=["Items"])
router.include_router(update_router, tags=["Items"])
router.include_router(delete_router, tags=["Items"])
router.include_router(search_name_router, tags=["Items"])
router.include_router(search_sku_router, tags=["Items"])
router.include_router(sort_price_router, tags=["Items"])
router.include_router(sort_name_router, tags=["Items"])
