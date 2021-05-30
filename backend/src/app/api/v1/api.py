from fastapi import APIRouter

from app.api.v1.endpoints import auth, pays, tests, users, admin

api_router = APIRouter()
api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(pays.router, prefix='/pays', tags=['pays'])
api_router.include_router(tests.router, prefix='/tests', tags=['tests'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(admin.router, prefix='/admin', tags=['admin'])
