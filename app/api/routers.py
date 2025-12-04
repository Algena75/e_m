from fastapi import APIRouter

from app.api.endpoints import object_router, user_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(object_router)
