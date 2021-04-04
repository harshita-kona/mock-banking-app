import json
from fastapi import APIRouter, Request, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.src.dependencies import check_apikey, get_db, get_current_active_user, get_current_user
from app.src.utils import get_error_code
from app import database, schemas
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
from typing import Optional
from app.src.config import get_config

SECRET_KEY = get_config()['key']
ALGORITHM = get_config()['algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES = get_config()['expire_token']

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()

@router.post('/signin/')
def user_signin(req:schemas.UserLogin ,db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    user=database.get_authenticated_user(db,req)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.customer_id}, expires_delta=access_token_expires
    )
    message={"access_token": access_token, "token_type": "bearer", "customer_id":user.customer_id}
    return JSONResponse(message)

@router.post('/signup/')
def user_signup(req:schemas.UserCreate ,db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    message=database.create_user(db=db,user= req)
    if message.user_no:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)

@router.post('/createbranch/')
def create_branch(req:schemas.BranchCreate ,db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    message=database.create_branch(db=db,branch= req)
    if message.branch_id:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)

@router.post('/createaccount/')
def create_user_account(req:schemas.AccountCreate,valid_user=Depends(get_current_user) ,db: Session = Depends(get_db), dependencies=Depends(check_apikey)):
    message=database.create_account(db=db,account= req)
    if message.account_no:
        message=get_error_code("success")
        message=jsonable_encoder(message)
    else:
        message=get_error_code("db_error")
        message=jsonable_encoder(message)

    return JSONResponse(message)



