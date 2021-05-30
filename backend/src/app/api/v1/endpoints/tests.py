from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app import schemas
from app.api import deps
from app.services import TestService

router = APIRouter()


@router.post('', response_model=schemas.Test)
async def create_test(
        test_info: schemas.TestCreate, db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Создание нового теста"""
    test = await TestService.create(db, user, test_info.external_id)
    return test


@router.get('', response_model=list[schemas.Test])
async def get_tests(
        db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Создание нового теста"""
    tests = await TestService.get_all_for_user(db, user)
    return tests


@router.get('/{test_uuid}', response_model=schemas.Test)
async def get_test(
        test_uuid: str, db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Получение теста"""
    test = await TestService.get(db, user, test_uuid)
    return test


@router.post('/{test_uuid}/pay', response_model=schemas.Test)
async def pay_test(
        test_uuid: str, db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Оплата теста"""
    test = await TestService.pay_test(db, user, test_uuid)
    return test


@router.get('/{test_uuid}/questions', response_model=list[schemas.Question])
async def get_test_questions(
        test_uuid: str, db: AsyncSession = Depends(deps.get_db),
        user: models.User = Depends(deps.get_current_user)
) -> Any:
    """Создание нового теста"""
    questions = await TestService.get_questions(db, user, test_uuid)
    return questions
