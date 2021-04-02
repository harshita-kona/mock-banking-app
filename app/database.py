from sqlalchemy.orm import Session
from uuid import uuid4
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "nothashed"
    db_user = models.Users(customer_id= str(uuid4()), email_id=user.email_id, first_name= user.first_name, middle_name= user.middle_name, last_name= user.last_name, date_of_birth= user.date_of_birth, occupation= user.occupation, mobile_no= user.mobile_no, created_date= user.created_date, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_branch(db: Session, branch: schemas.BranchCreate):
    db_branch = models.Branches(branch_id= str(uuid4()), branch_name=branch.branch_name, branch_city= branch.branch_city, created_date=branch.created_date)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Accounts(account_no= str(uuid4()), customer_id=account.customer_id, branch_id= account.branch_id, opening_balance= account.opening_balance, current_balance= account.current_balance, account_type= account.account_type, account_status= account.account_status, account_created_date= account.account_created_date)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_current_balance(db: Session, transaction):
    account=db.query(models.Accounts).filter(models.Accounts.account_no == transaction.account_no).first()
    if transaction.transaction_type=="Withdrawal":
        if account.current_balance<transaction.amount:
            return False
        else:
            account.current_balance=account.current_balance-transaction.amount
            db.commit()
    else:
        account.current_balance=account.current_balance+transaction.amount
        db.commit()
    return True

def add_user_transaction(db: Session, transaction: schemas.TransactionCreate):
    if update_current_balance(db,transaction):
        db_transaction = models.Transactions(transaction_no= str(uuid4()), account_no=transaction.account_no, medium_of_transaction= transaction.medium_of_transaction, transaction_type=transaction.transaction_type,amount= transaction.amount, transaction_date=transaction.transaction_date)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        return db_transaction
    else:
        return False

