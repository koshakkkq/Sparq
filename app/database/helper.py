from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)


from app.config.settings import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    print("ERROR!!!!!!!!!!!!!!!")
    engine = create_async_engine(settings.database_url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
