import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class TestBase(BaseModel):
    external_id: int


class TestCreate(TestBase):
    pass


class TestInDBBase(TestBase):
    uuid: UUID4
    created_at: Optional[datetime.datetime]
    status: Optional[int]

    class Config:
        orm_mode = True


class Test(TestInDBBase):
    is_paid: bool
    title: Optional[str]
    cost: int


class QuestionBase(BaseModel):
    type: int
    rubric: Optional[str]
    body: str
    answers: list[str]


class QuestionInDBBase(QuestionBase):
    pass

    class Config:
        orm_mode = True


class Question(QuestionInDBBase):
    pass

#
# class UserUpdate(UserBase):
#     password: Optional[str] = None
#
#
# class UserInDBBase(UserBase):
#     id: Optional[int] = None
#
#     class Config:
#         orm_mode = True
#
#
# class User(UserInDBBase):
#     pass
#
#
# class UserInDB(UserInDBBase):
#     hashed_password: str
