from api.orders.endpoints import orders
from fastapi import APIRouter

orders_router = APIRouter()
orders_router.include_router(orders.router)