import datetime

from pydantic import BaseModel


class Status(BaseModel):
    value: str
    changedDateTime: datetime.datetime


class Customer(BaseModel):
    email: str
    account: str


class Bill(BaseModel):
    siteId: str
    billId: str
    status: Status
    customer: Customer


class QiwiCallback(BaseModel):
    bill: Bill
    version: str
