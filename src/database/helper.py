from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src.config.settings import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    logger.info("Creating database engine and session factory.")

    engine = create_async_engine(settings.database_url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        logger.debug("Database session started.")
        try:
            yield session
            await session.commit()
            logger.debug("Transaction committed successfully.")
        except exc.SQLAlchemyError:
            await session.rollback()
            logger.error(f"Transaction rolled back due to error: {e}")
            raise
        finally:
            logger.debug("Database session closed.")
