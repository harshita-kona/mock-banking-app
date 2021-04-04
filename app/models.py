from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    user_no = Column(Integer, primary_key=True, autoincrement="auto")
    customer_id = Column(String, unique=True, index=True)
    email_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    occupation = Column(String)
    mobile_no = Column(String)
    created_date = Column(DateTime)
    password = Column(String)

    accounts = relationship("Accounts", back_populates="user_account")


class Branches(Base):
    __tablename__ = "branches"

    branch_no = Column(Integer, primary_key=True, autoincrement="auto")
    branch_id = Column(String, unique=True)
    branch_name = Column(String)
    branch_city = Column(String)
    created_date = Column(DateTime)

    branches = relationship("Accounts", back_populates="account_branch")

class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement="auto")
    account_no = Column(String, unique=True)
    customer_id = Column(String, ForeignKey("users.customer_id"))
    branch_id = Column(String, ForeignKey("branches.branch_id"))
    opening_balance=Column(Integer)
    current_balance=Column(Integer)
    account_type=Column(String)
    account_status = Column(String)
    account_created_date = Column(DateTime, index=True)
    
    user_account = relationship("Users", back_populates="accounts")
    account_branch = relationship("Branches", back_populates="branches")
    transactions = relationship("Transactions", back_populates="transaction_by")

class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement="auto")
    transaction_no = Column(String)
    account_no = Column(String,ForeignKey("accounts.account_no"))
    medium_of_transaction = Column(String)
    transaction_type = Column(String)
    amount = Column(Integer)
    balance=Column(Integer)
    transaction_date = Column(DateTime, index=True)

    transaction_by = relationship("Accounts", back_populates="transactions")
