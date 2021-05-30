import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class PayBase(BaseModel):
    type: int
    description: str = ''
    value: float


class PayCreate(PayBase):
    user_id: int
    order_id: Optional[str]


class PayInDBBAse(PayBase):
    uuid: UUID4

    class Config:
        orm_mode = True


class Pay(PayInDBBAse):
    created_at: datetime.datetime
