from fastapi import APIRouter
from routers.provider.add import router as add_provider_router
from routers.provider.delete import router as delete_provider_router

provider_router = APIRouter()

# ثبت routeهای مربوط به provider
provider_router.include_router(add_provider_router)
provider_router.include_router(delete_provider_router)