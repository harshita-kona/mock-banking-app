import json
from fastapi import APIRouter, Request, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.src.dependencies import check_apikey, get_db
from app.src.utils import get_error_code
from app import database, schemas
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/signup/')
def account_signup(req:schemas.UserCreate ,db: Session = Depends(get_db)):
    message=database.create_user_account(db=db,user= req)
    if message.user_no:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)