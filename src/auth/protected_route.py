# src/protected_route.py
from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}