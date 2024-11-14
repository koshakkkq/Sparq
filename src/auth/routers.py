# src/auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import timedelta
from src.database.helper import get_db_session
from src.auth.models import User
from src.auth.utils import hash_password, verify_password, create_access_token
from src.database.repository import DatabaseRepository

router = APIRouter(prefix="/auth", tags=["auth"])


# Схемы для запросов
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    # Проверка на существование пользователя
    existing_user = await session.execute(select(User).filter(User.username == user.username))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Хешируем пароль и создаем пользователя
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "User created successfully"}


@router.post("/login")
async def login_user(user: UserLogin, session: AsyncSession = Depends(get_db_session)):
    # Проверка пользователя
    result = await session.execute(select(User).filter(User.username == user.username))
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Создаем JWT токен
    access_token = create_access_token({"sub": db_user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}