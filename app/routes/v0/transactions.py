import json
from fastapi import APIRouter, Request, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.src.dependencies import check_apikey, get_db
from app.src.utils import get_error_code
from app import database, schemas
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/addtransaction/')
def account_signup(req:schemas.TransactionCreate ,db: Session = Depends(get_db)):
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