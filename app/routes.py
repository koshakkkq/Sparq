from fastapi import APIRouter, HTTPException

from .auth.routers import router as auth_routers
from .auth.protected_route import router as protected_router
from .chat.routers import router as chat_router


def get_app_router():
    router = APIRouter()
    router.include_router(auth_routers)
    router.include_router(protected_router)
    router.include_router(chat_router)
    # router.include_router(websocket_router)
    return router
