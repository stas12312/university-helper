import uuid
from typing import TYPE_CHECKING

import uuid as uuid
from sqlalchemy import Column, Boolean, String, Integer, DateTime, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .pay import Pay  # noqa
    from .test import Test  # noqa


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    balance = Column(Float, nullable=False, default=0)

    tests = relationship('Test', back_populates='user')
    pays = relationship('Pay', back_populates='user')

    __mapper_args__ = {"eager_defaults": True}


class EmailVerify(Base):
    __tablename__ = 'email_verifies'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String)
    code = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expired_at = Column(DateTime(timezone=True))
