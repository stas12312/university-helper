from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api import deps
from app.schemas import Pay
from app.services import PayServce

router = APIRouter()


@router.get('/pays', response_model=list[Pay])
async def get_pays(
        db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Получение платежей пользователя"""
    pays = await PayServce.get_user_pays(db, user.id)
    return pays
