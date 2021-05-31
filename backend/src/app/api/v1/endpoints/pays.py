from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api import deps
from app.schemas import Pay, PayRequest, QiwiCallback
from app.services import PayServce, QiwiService

router = APIRouter()


@router.get('', response_model=list[Pay])
async def get_pays(
        db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Получение платежей пользователя"""
    pays = await PayServce.get_user_pays(db, user.id)
    return pays


@router.post('')
async def create_pay(
        pay_request: PayRequest,
        db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)

) -> Any:
    """Создание запроса на оплату"""

    pay = await PayServce.add_pay(db, models.Pay.ADD_MONEY, f'Пополнение баланса через Qiwi {user.email}',
                                  pay_request.amount,
                                  user.id, models.Pay.CREATED)
    data = await QiwiService.create_account(user, pay.value, pay.uuid)
    return data


@router.get('/{uuid}/pay-status')
async def get_pay_status(
        uuid: str,
        db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    pass


@router.post('/callback')
async def process_callback(
        callback: QiwiCallback,
        db: AsyncSession = Depends(deps.get_db),

) -> Any:
    """Обработка колюэка от платёжной системы"""
    if callback.bill.status.value == 'WAITING':
        pass
    elif callback.bill.status.value == 'PAID':
        await PayServce.process_success_pay(db, callback.bill.billId)
    else:
        await PayServce.process_error_pay(db, callback.bill.billId)
    return {'message': 'ok'}
