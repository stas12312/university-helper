import random
import typing
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import User, EmailVerify


class UserService:

    @classmethod
    async def create(cls, db: AsyncSession, email: str,
                     password: str, is_superuser: bool = False) -> typing.Optional[User]:
        """Добавление пользователя"""
        user = await cls.get_by_email(db, email)
        if user:
            return None

        result = await db.execute(
            insert(User)
                .values(email=email, password=get_password_hash(password),
                        created_at=datetime.now(), last_login=datetime.now(),
                        balance=0, is_active=True, is_superuser=is_superuser).returning(User.id)
        )
        user_id = result.scalar_one()
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one()
        if settings.START_BALANCE > 0:
            await services.PayServce.add_pay(db, 2, 'Начисление бонусов за регистрацию',
                                             settings.START_BALANCE, user.id)

        await db.commit()
        return user

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> typing.Optional[User]:
        """Получение пользователя по email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @classmethod
    async def get(cls, db: AsyncSession, user_id: int) -> typing.Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @classmethod
    async def auth(cls, db: AsyncSession, email: str, password: str) -> typing.Optional[User]:
        """Авторизация пользователя"""
        result = await db.execute(select(User).where(User.email == email))
        user: User = result.scalars().first()

        if user and verify_password(password, user.password):
            user.last_login = datetime.now()
            await db.commit()
            return user
        return None

    @classmethod
    async def send_email_code(cls, email: str):
        """Отправка кода подтверждения"""
        pass

    @classmethod
    async def register(cls, db: AsyncSession, email: str, password: str, verify_uuid: str, verify_code: int) -> User:
        """Регистрация пользователя"""
        if not await EmailVerifyService.verify(db, email, verify_uuid, verify_code):
            raise HTTPException(status_code=400, detail='Неверный проверочный код')
        user = await cls.create(db, email, password)
        return user


class EmailVerifyService:
    @classmethod
    async def _exist_verify(cls, db: AsyncSession, email: str) -> typing.Optional[EmailVerify]:
        """Проверка, что код уже был отправлен"""
        now = datetime.now()
        result = await db.execute(
            select(EmailVerify)
                .where(EmailVerify.email == email, EmailVerify.expired_at >= now)
        )

        return result.scalars().first()

    @classmethod
    async def create(cls, db: AsyncSession, email: str) -> EmailVerify:
        from app.services import EmailService

        if await UserService.get_by_email(db, email):
            raise HTTPException(status_code=400, detail='Email занят')

        exist_verify = await cls._exist_verify(db, email)
        if exist_verify:
            raise HTTPException(status_code=400, detail='Проверочный код уже отправлен на почту')
        expired = datetime.now() + timedelta(minutes=1)

        result = await db.execute(insert(EmailVerify).values(email=email, expired_at=expired,
                                                             code=random.randint(100000, 999999))
                                  .returning(EmailVerify.uuid))
        email_verify_uuid = result.scalar_one()
        result = await db.execute(
            select(EmailVerify)
                .where(EmailVerify.uuid == email_verify_uuid)
        )
        await db.commit()
        email_verify = result.scalars().first()
        await EmailService.send_verify_email_code(email, email_verify.code)

        return email_verify

    @classmethod
    async def verify(cls, db: AsyncSession, email: str, verify_uuid: str, verify_code: int) -> bool:
        """Проверка кода"""
        result = await db.execute(select(EmailVerify).where(EmailVerify.email == email,
                                                            EmailVerify.uuid == verify_uuid))

        verify = result.scalars().first()
        if not verify:
            return False

        if verify.code == verify_code:
            await db.execute(delete(EmailVerify).where(EmailVerify.uuid == verify_uuid))
            return True
        return False
