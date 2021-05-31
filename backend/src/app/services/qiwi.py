import datetime

import aiohttp

from app.core.config import settings
from app.models import User


class QiwiService:

    @classmethod
    async def create_account(cls, user: User, amount: float, pay_uuid: str) -> dict:
        """Выставление счёта на оплату"""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        exparation = now + datetime.timedelta(days=1)
        headers = {
            'Authorization': f'Bearer {settings.QIWI_PRIVATE_KEY}'
        }
        data = {
            'amount': {
                'value': amount,
                'currency': 'RUB',
            },
            'expirationDateTime': exparation.isoformat(),
            'customer': {
                'email': user.email,
                'account': user.id,
            },
            'comment': f'Пополнение баланса на {amount} рублей {user.email}',
            'customFields': {'themeCode': 'Stanyslav-RYJqa_xwJq'}
        }
        async with aiohttp.ClientSession() as session:
            async with session.put(f'https://api.qiwi.com/partner/bill/v1/bills/{pay_uuid}',
                                   json=data, headers=headers) as r:
                return await r.json()
