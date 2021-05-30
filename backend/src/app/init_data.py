import asyncio
import logging

from app.db.init_db import init_db
from app.db.session import async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    db = async_session()
    await init_db(db)
    await db.close()


async def main() -> None:
    logger.info("Инициализация БД данными")
    await init()
    logger.info("Инициализация завершена")


if __name__ == "__main__":
    asyncio.run(main())
