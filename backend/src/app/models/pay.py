import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, BigInteger, DateTime, String, Integer, ForeignKey, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa


class Pay(Base):
    __tablename__ = 'pays'
    __table_args__ = {'extend_existing': True}

    REPLENISHMENT = 0  # Пополнение
    PAYMENT = 1  # Оплата
    ADD_BONUSE = 2  # Начисление бонусов
    ADD_MONEY = 3  # Добавление денег

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(String, nullable=True)
    type = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship('User', back_populates='pays')
