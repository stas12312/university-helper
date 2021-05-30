from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app import schemas
from app.core import security
from app.core.config import settings
from app.db.session import async_session
from app.services.user import UserService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_current_user(
        db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недействительные учётные данные",
        )
    user = await UserService.get(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
