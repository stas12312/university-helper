from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

engine = create_engine(settings.SYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
