import json
from fastapi import APIRouter, Request, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.src.dependencies import check_apikey, get_db, get_current_user, get_current_active_user
from app.src.utils import get_error_code
from app import database, schemas
from sqlalchemy.orm import Session

router = APIRouter()

"""
API to add transaction of the user
"""
@router.post('/addtransaction/')
def add_transaction(req:schemas.TransactionCreate, active_user=Depends(get_current_active_user),valid_user=Depends(get_current_user),db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    message=database.add_user_transaction(db=db,transaction= req)
    if not message:
        message=get_error_code("insufficient_balance")
        message=jsonable_encoder(message)
    elif message.transaction_id:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)


"""
API to get last n transactions of the account
"""
@router.post('/lastntransactions/')
def get_last_n_transactions(req:schemas.LastnTransactions, active_user=Depends(get_current_active_user), valid_user=Depends(get_current_user),db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    message=database.get_n_transactions(db=db,transaction= req)
    message=jsonable_encoder(message)
    return JSONResponse(message)


"""
API to get all the transactions done between the two dates
"""
@router.post('/transactionsbydate/')
def get_transactions_by_date(req:schemas.TransactionsBetweenDates, active_user=Depends(get_current_active_user), valid_user=Depends(get_current_user),db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    message=database.get_transactions_between_dates(db=db,transaction= req)
    message=jsonable_encoder(message)

    return JSONResponse(message)
    