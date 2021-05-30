"""
Получение правильных ответов из dispace
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# def get_test(test_id: int) -> dict:
#     """Получение теста"""
#     uri = f'https://dispace.edu.nstu.ru/ditest/index/offline/html/{test_id}'
#     questions = parse.get_answers(uri)
#
#     test = parse.get_test_with_answers(test_id)
#     test.questions = sorted(test.questions, key=lambda x: x.id)
#     questions_data = []
#     for question in test.questions:
#         questions_data.append({
#             'id': question.id,
#             'rubric': question.rubric,
#             'text': question.text,
#             'answers': question.answers
#         })
#
#     if not questions:
#         raise HTTPException(status_code=404, detail='Тест на найден')
#
#     test = {
#         'id': test.id,
#         'title': test.title,
#         'questions': questions_data,
#     }
#     return test
#
#
# @app.get('/{test_id}')
# async def get_answers(test_id: int):
#     return get_test(test_id)
