from typing import Annotated

from fastapi import APIRouter, Depends

from src.database import DatabaseRepository, get_repository
import src.models.test_model as db_models
from .models import TestModelPayload, TestModel

router = APIRouter(prefix="/auth", tags=["chat"])


TestModelRepository = Annotated[
    DatabaseRepository[db_models.TestModel],
    Depends(get_repository(db_models.TestModel)),
]


@router.post("/test_model")
async def add_date(
    data: TestModelPayload,
    repository: TestModelRepository,
) -> TestModel:
    logger.debug(f"Payload data: {data}")

    test_model = await repository.create(data.model_dump())

    return TestModel.model_validate(test_model)
