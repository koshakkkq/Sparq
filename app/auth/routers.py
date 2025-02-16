import asyncio
# src/auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status, Form,Response,Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import timedelta
from app.database.helper import get_db_session
from app.models import User
from app.auth.utils import hash_password, verify_password, create_access_token
from app.database.repository import DatabaseRepository
from sqlalchemy.future import select
from app.auth.session import create_session, get_session, clear_session
router = APIRouter(prefix="/auth", tags=["auth"])


# Схемы для запросов
class UserCreateModel(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register_user(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_db_session),
):
    # Проверяем, существует ли пользователь с таким username
    existing_user = await session.execute(
        select(User).filter(User.username == user_data.username)
    )
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Хешируем пароль и создаем нового пользователя
    hashed_password = hash_password(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login_user(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db_session),
):
    # Ищем пользователя
    result = await session.execute(select(User).filter(User.username == username))
    db_user = result.scalars().first()

    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Создаем сессию
    create_session(response, username)
    return {"message": f"Welcome, {username}!"}

@router.post("/logout")
async def logout_user(response: Response):
    clear_session(response)
    return {"message": "You have been logged out"}