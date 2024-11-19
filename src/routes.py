from fastapi import APIRouter

# from .websockets.routers import router as websocket_router
from .auth.routers import router as auth_routers
from .auth.protected_route import router as protected_router

def get_app_router():
    router = APIRouter()
    router.include_router(auth_routers)
    router.include_router(protected_router)
    return router
