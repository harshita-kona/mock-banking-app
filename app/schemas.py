from typing import List, Optional
from pydantic import BaseModel
import datetime

class TransactionBase(BaseModel):
    account_no: str

class LastnTransactions(BaseModel):
    account_no: str
    limit:int

class TransactionsBetweenDates(BaseModel):
    account_no: str
    start_date:datetime.date
    end_date:datetime.date


class TransactionCreate(TransactionBase):
    medium_of_transaction: str
    transaction_type: str
    amount: int
    transaction_date: datetime.datetime


class Transaction(TransactionBase):
    transaction_no: int
    transaction_id: str

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
    mobile_no: str
    date_of_birth: datetime.date
    created_date: datetime.datetime


class User(UserBase):
    user_no: int
    customer_id: str
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True


class BranchBase(BaseModel):
    branch_name: str
    branch_city: str
    created_date: datetime.datetime


class BranchCreate(BranchBase):
    pass


class Branch(BranchBase):
    branch_no: int
    branch_id: str
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    customer_id: str


class AccountCreate(AccountBase):
    branch_id: str
    opening_balance: int
    current_balance: int
    account_type: str
    account_status: str
    account_created_date: datetime.datetime


class Account(AccountBase):
    account_no: int
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True



