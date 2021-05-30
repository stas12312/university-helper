import datetime

from fastapi import HTTPException
from sqlalchemy import insert, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Pay
from app.services import UserService


class PayServce:

    @classmethod
    async def add_pay(cls, db: AsyncSession, type_: int, description: str, value: float, user_id: int) -> Pay:
        """Добавление платежа"""
        result = await db.execute(insert(Pay).values(
            type=type_,
            description=description,
            value=value,
            user_id=user_id,
            created_at=datetime.datetime.now(tz=datetime.timezone.utc)
        ).returning(Pay.uuid))
        pay_uuid = result.scalar_one()
        if type_ == Pay.PAYMENT:
            value = -value

        user = await UserService.get(db, user_id)
        user.balance += value
        if user.balance < 0:
            raise HTTPException(status_code=400, detail='Недостаточно средст на балансе')

        await db.commit()

        result = await db.execute(select(Pay).where(Pay.uuid == pay_uuid))
        return result.scalar_one()

    @classmethod
    async def get_user_pays(cls, db: AsyncSession, user_id: int) -> list[Pay]:
        """Получение платежей пользователя"""
        result = await db.execute(select(Pay).where(Pay.user_id == user_id).order_by(desc(Pay.created_at)))
        return result.scalars().all()
