import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, BigInteger, DateTime, Boolean, String, Integer, ForeignKey, Float, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .pay import Pay  # noqa
    from .user import User  # noqa


class Test(Base):
    __tablename__ = 'tests'
    __table_args__ = {'extend_existing': True}
    IN_QUEUE = 1
    IN_PROCESS = 2
    SUCCESS = 3
    ERROR = 4

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    external_id = Column(BigInteger)
    is_paid = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, default='')
    cost = Column(Float, default=0)
    pay_uuid = Column(UUID(as_uuid=True), ForeignKey('pays.uuid'), nullable=True)
    status = Column(Integer, default=IN_QUEUE)

    questions = relationship('Question', back_populates='test')
    user = relationship('User', back_populates='tests')

    __mapper_args__ = {"eager_defaults": True}


class Question(Base):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    external_id = Column(BigInteger, nullable=False)
    type = Column(Integer)
    test_id = Column(UUID(as_uuid=True), ForeignKey('tests.uuid'))
    rubric = Column(String)
    body = Column(String)
    answers = Column(JSON)

    test = relationship('Test', back_populates='questions')
    __mapper_args__ = {"eager_defaults": True}
