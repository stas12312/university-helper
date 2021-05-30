from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db import base  # noqa: F401
from app.services.user import UserService


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=async_engine)
    print('Проверка', settings.FIRST_SUPERUSER_PASSWORD)
    user = await UserService.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:

        user = await UserService.create(db, email=settings.FIRST_SUPERUSER,
                                        password=settings.FIRST_SUPERUSER_PASSWORD, is_superuser=True)
