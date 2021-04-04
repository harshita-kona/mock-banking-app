from fastapi import Header, HTTPException, Depends, status
from app.src.config import get_config
from app.connect_database import SessionLocal,engine
from app import database
from fastapi.security import OAuth2PasswordBearer
from app import schemas
from sqlalchemy.orm import Session
from jose import jwt, JWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def check_apikey(api_key:str=Header(None, convert_underscores=False)):
    key=get_config()['api_key']
    if api_key!=key:
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id: str = payload.get("sub")
        if customer_id is None:
            raise credentials_exception
        user=database.get_user_from_id(db,customer_id)
        if not user:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return True


async def get_current_active_user(current_user: schemas.User,db: Session = Depends(get_db)):
    user=database.get_user_from_id(db,current_user.customer_id)
    if not user or user.account_status=="INACTIVE":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user