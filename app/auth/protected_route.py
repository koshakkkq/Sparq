# src/protected_route.py
from fastapi import APIRouter, Depends, Request
from app.auth.dependencies import get_current_user
from app.auth.session import create_session, get_session, clear_session
router = APIRouter()

@router.get("/protected")
async def protected_page(request: Request):
    session_data = get_session(request)
    if not session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return {"message": f"Welcome back, {session_data['username']}!"}