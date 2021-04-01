from fastapi import Header, HTTPException
from app.src.config import get_config
from app.connect_database import SessionLocal,engine

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

