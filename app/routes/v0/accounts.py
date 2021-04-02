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
def user_signup(req:schemas.UserCreate ,db: Session = Depends(get_db)):
    message=database.create_user(db=db,user= req)
    if message.user_no:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)

@router.post('/createbranch/')
def create_branch(req:schemas.BranchCreate ,db: Session = Depends(get_db)):
    message=database.create_branch(db=db,branch= req)
    if message.branch_id:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)

@router.post('/createaccount/')
def create_user_account(req:schemas.AccountCreate ,db: Session = Depends(get_db)):
    message=database.create_account(db=db,account= req)
    if message.account_no:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)



