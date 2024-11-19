import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import DatabaseRepository, get_repository
import src.models.test_model as db_models
from src.models.base_model import get_db


router = APIRouter(prefix="/auth", tags=["chat"])


TestModelRepository = Annotated[
    DatabaseRepository[db_models.TestModel],
    Depends(get_repository(db_models.TestModel)),
]


@router.get("/add_date/")
async def add_date(db: AsyncSession = Depends(get_db)):
    new_entry = TestModelRepository.TestModel(timestamp=datetime.utcnow())

    db.add(new_entry)
    await db.commit()  # Асинхронный commit
    await db.refresh(new_entry)  # Асинхронное обновление записи

    return {"id": new_entry.id, "timestamp": new_entry.timestamp}
