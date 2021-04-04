from sqlalchemy.orm import Session
from uuid import uuid4
from . import models, schemas
import datetime
from app.src import utils

"""
Sign up user for the application
"""
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.Users(customer_id= str(uuid4()), email_id=user.email_id, first_name= user.first_name, middle_name= user.middle_name, last_name= user.last_name, date_of_birth= user.date_of_birth, occupation= user.occupation, mobile_no= user.mobile_no, created_date= user.created_date, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

"""
Check if the user is authorised
"""
def get_authenticated_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.Users).filter(models.Users.email_id == user.email_id).first()
    if not db_user:
        return False
    if not utils.verify_password(user.password, db_user.password):
        return False
    return db_user

"""
Get user details from the customer ID
"""
def get_user_from_id(db: Session, customer_id: str):
    db_user = db.query(models.Users).filter(models.Users.customer_id == customer_id).first()
    if not db_user:
        return False
    return db_user


"""
Create a branch for the application
"""
def create_branch(db: Session, branch: schemas.BranchCreate):
    db_branch = models.Branches(branch_id= str(uuid4()), branch_name=branch.branch_name, branch_city= branch.branch_city, created_date=branch.created_date)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

"""
Create an account for the user
"""
def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Accounts(account_no= str(uuid4()), customer_id=account.customer_id, branch_id= account.branch_id, opening_balance= account.opening_balance, current_balance= account.current_balance, account_type= account.account_type, account_status= account.account_status, account_created_date= account.account_created_date)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

"""
Update current balance of the user's account
"""
def update_current_balance(db: Session, transaction):
    account=db.query(models.Accounts).filter(models.Accounts.account_no == transaction.account_no).first()
    if transaction.transaction_type=="Withdrawal":
        if account.current_balance<transaction.amount:
            return (False,account.current_balance)
        else:
            account.current_balance=account.current_balance-transaction.amount
            db.commit()
    else:
        account.current_balance=account.current_balance+transaction.amount
        db.commit()
    return (True,account.current_balance)

"""
Add user transaction to the database
"""
def add_user_transaction(db: Session, transaction: schemas.TransactionCreate):
    (status,balance)=update_current_balance(db,transaction)
    if status:
        db_transaction = models.Transactions(transaction_no= str(uuid4()), account_no=transaction.account_no, medium_of_transaction= transaction.medium_of_transaction, transaction_type=transaction.transaction_type,amount= transaction.amount, balance=balance, transaction_date=transaction.transaction_date)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    else:
        return False

"""
Get last n transactions of the account
"""
def get_n_transactions(db: Session, transaction):
    transactions=db.query(models.Transactions).filter(models.Transactions.account_no == transaction.account_no).order_by(models.Transactions.transaction_date.desc()).limit(transaction.limit).all()
    return transactions

"""
Get the transactions done between the two dates
"""
def get_transactions_between_dates(db: Session, transaction):
    transaction.start_date=datetime.datetime(transaction.start_date.year, transaction.start_date.month, transaction.start_date.day, 0, 0,0)
    transaction.end_date=datetime.datetime(transaction.end_date.year, transaction.end_date.month, transaction.end_date.day, 23, 59,59)
    transactions=db.query(models.Transactions).filter(models.Transactions.account_no == transaction.account_no).filter(models.Transactions.transaction_date >= transaction.start_date).filter(models.Transactions.transaction_date <= transaction.end_date).all()
    return transactions

