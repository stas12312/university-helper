from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services import UserService, EmailVerifyService

router = APIRouter()


@router.post('/auth/login', response_model=schemas.Token)
async def auth(
        db: AsyncSession = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await UserService.auth(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        'access_token': security.create_access_token(
            user.id, access_token_expires
        ),
        'token_type': 'bearer',
    }


@router.post('/auth/send-code')
async def send_verify_code(user: schemas.UserEmail,
                           db: AsyncSession = Depends(deps.get_db),
                           ) -> Any:
    """Отправка проверочного кода"""
    verify_email = await EmailVerifyService.create(db, user.email)
    return verify_email


@router.post('/auth/register', response_model=schemas.Token)
async def register(user: schemas.UserCreate,
                   db: AsyncSession = Depends(deps.get_db)
                   ) -> Any:
    """Регистрация пользователя"""
    user = await UserService.register(db, user.email, user.password, user.verify_uuid, user.verify_code)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': security.create_access_token(
            user.id, access_token_expires
        ),
        'token_type': 'bearer',
    }


@router.get('/auth/me', response_model=schemas.User)
async def get_me(
        db: AsyncSession = Depends(deps.get_db), user: models.User = Depends(deps.get_current_user)
) -> Any:
    return user
