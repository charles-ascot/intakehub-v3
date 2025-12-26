"""Database connection setup"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings
import logging

logger = logging.getLogger(__name__)

engine = None
AsyncSessionLocal = None

async def init_db():
    global engine, AsyncSessionLocal
    db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(db_url, echo=settings.environment == "development")
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    logger.info(f"✅ Connected to database")

async def get_db():
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
