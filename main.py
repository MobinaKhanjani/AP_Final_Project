from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers.auth import router as auth_router
from routers.item import router as items_router
from routers.order import router as orders_router
from routers.reports import router as reports_router


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
    allow_origins=["*"],  # در production دامنه‌های خاص رو قرار بده
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# رویداد راه‌اندازی
@app.on_event("startup")
async def on_startup():
    init_db()
    print("✅ Database initialized successfully")

# شامل کردن روترها
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "خوش آمدید به سیستم مدیریت موجودی",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "items": "/items",
            "orders": "/orders",
            "transactions": "/transactions",
            "reports": "/reports"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "OK",
        "message": "سیستم فعال و سالم است",
        "database": "Connected"
    }

@app.get("/info", tags=["Info"])
async def api_info():
    return {
        "name": "Inventory Management System",
        "description": "سیستم مدیریت موجودی و انبارداری",
        "version": "1.0.0",
        "author": "Your Team",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
from routers import add_item, delete_item, edit_item

app = FastAPI()

app.include_router(add_item.router, tags=["Item"])
app.include_router(delete_item.router, tags=["Item"])
app.include_router(edit_item.router, tags=["Item"])