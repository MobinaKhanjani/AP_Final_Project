from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers.auth import router as auth_router
from routers.reports import router as reports_router
from routers.supplier_orders import router as supplier_orders_router
from routers.customer_order import router as customer_orders_router
from routers.item import router as items_router
from routers.provider import router as providers_router

app = FastAPI(
    title="Inventory Management API",
    description="سیستم مدیریت موجودی و انبار",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# رویداد راه‌اندازی
@app.on_event("startup")
async def on_startup():
    init_db()
    print("✅ Database initialized successfully")

# شامل کردن همه روترها
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(providers_router, prefix="/provider", tags=["Providers"])
app.include_router(items_router, prefix="/item", tags=["Items"])
app.include_router(supplier_orders_router, prefix="/supplier_orders", tags=["Supplier Orders"])
app.include_router(customer_orders_router, prefix="/customer_order", tags=["Customer Orders"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "خوش آمدید به سیستم مدیریت موجودی",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "reports": "/reports",
            "supplier_orders": "/api/supplier-orders",
            "customer_orders": "/api/customer-orders",
            "items": "/api/items",
            "providers": "/api/providers"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "OK",
        "message": "سیستم فعال و سالم است",
        "database": "Connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from database import init_db
# from routers.auth import router as auth_router
# from routers.reports import router as reports_router
# from routers.supplier_orders import router as supplier_orders_router
# app = FastAPI(
#     title="Inventory Management API",
#     description="سیستم مدیریت موجودی و انبار",
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # تنظیمات CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # رویداد راه‌اندازی
# @app.on_event("startup")
# async def on_startup():
#     init_db()
#     print("✅ Database initialized successfully")

# # شامل کردن روترها
# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(reports_router, prefix="/reports", tags=["Reports"])

# @app.get("/", include_in_schema=False)
# async def root():
#     return {
#         "message": "خوش آمدید به سیستم مدیریت موجودی",
#         "version": "1.0.0",
#         "docs": "/docs",
#         "endpoints": {
#             "auth": "/auth",
#             "reports": "/reports"
#         }
#     }

# @app.get("/health", tags=["Health"])
# async def health_check():
#     return {
#         "status": "OK",
#         "message": "سیستم فعال و سالم است",
#         "database": "Connected"
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)