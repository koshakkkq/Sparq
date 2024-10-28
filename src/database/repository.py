import uuid
from collections.abc import Callable
from typing import Generic, TypeVar

from fastapi import Depends
from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base_model import Base as ModelBase
from src.database.helper import get_db_session

Model = TypeVar("Model", bound=ModelBase)


class DatabaseRepository(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        async with self.session as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance

    async def get(self, pk: uuid.UUID) -> Model | None:
        return await self.session.get(self.model, pk)

    async def filter(
        self,
        *expressions: BinaryExpression,
    ) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))


def get_repository(
    model: type[ModelBase],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(model, session)

    return func
