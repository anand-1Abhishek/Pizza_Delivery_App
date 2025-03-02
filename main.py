from fastapi import FastAPI
from api.auth import auth_router
from api.orders import orders_router
from core.config import settings
from db.base import Base
from db.session import engine

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Order Management API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Include routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth")
app.include_router(orders_router, prefix=f"{settings.API_V1_STR}/orders")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)