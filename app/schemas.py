from typing import List, Optional
from pydantic import BaseModel
import datetime

class TransactionBase(BaseModel):
    transaction_date: datetime.date
    amount: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transaction_no: int
    user_id: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email_id: str

class UserCreate(UserBase):
    password: str
    first_name: str
    middle_name: str
    last_name: str
    occupation: str
    mobile_no: int
    date_of_birth: datetime.date
    created_date: datetime.datetime

class User(UserBase):
    user_no: int
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True
