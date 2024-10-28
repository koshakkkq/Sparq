from fastapi import APIRouter

# from .websockets.routers import router as websocket_router
from .auth.routers import router as auth_routers


def get_app_router():
    router = APIRouter()
    router.include_router(auth_routers)
    return router
