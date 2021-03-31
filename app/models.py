from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class Users(Base):
    __tablename__ = "users"

    user_no = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    email_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    occupation = Column(String)
    mobile_no = Column(Integer)
    created_date = Column(Date)
    hashed_password = Column(String)

    transactions = relationship("Transactions", back_populates="transaction_by")


class Transactions(Base):
    __tablename__ = "transactions"

    transaction_no = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String)
    amount = Column(Integer)
    transaction_date = Column(Date, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    transaction_by = relationship("Users", back_populates="transactions")
