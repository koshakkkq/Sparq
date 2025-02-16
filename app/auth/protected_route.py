# src/protected_route.py
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
)
from app.auth.session import get_session

router = APIRouter()


@router.get("/protected")
async def protected_page(request: Request):
    session_data = get_session(request)
    if not session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return {"message": f"Welcome back, {session_data['username']}!"}
