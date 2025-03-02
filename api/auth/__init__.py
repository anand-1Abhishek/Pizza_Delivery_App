from fastapi import APIRouter
from api.auth.endpoints import login, users

auth_router = APIRouter()
auth_router.include_router(login.router, prefix="/login")
auth_router.include_router(users.router, prefix="/users")