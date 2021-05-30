from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api import deps
from app.schemas import PayCreate
from app.services import PayServce

router = APIRouter()


@router.post('/users/add-money')
async def add_money_to_user(pay: PayCreate, db: AsyncSession = Depends(deps.get_db),
                            user: models.User = Depends(deps.get_current_user)):
    """Добавление денег пользователю"""
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='У вас нет доступа')

    pay = await PayServce.add_pay(db, pay.type, pay.description, pay.value, pay.user_id)

    return pay
