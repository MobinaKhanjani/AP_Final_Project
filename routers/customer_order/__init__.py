from fastapi import APIRouter
from .list import router as list_router
from .create import router as create_router
from .get import router as get_router
from .update import router as update_router

router = APIRouter()
router.include_router(list_router, tags=["Customer Orders"])
router.include_router(create_router, tags=["Customer Orders"])
router.include_router(get_router, tags=["Customer Orders"])
router.include_router(update_router, tags=["Customer Orders"])
