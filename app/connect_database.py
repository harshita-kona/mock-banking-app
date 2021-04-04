from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import models
from app.src.config import get_config

pg_conf=get_config()['postgres_conf']

DATABASE_URL = "postgresql://"+pg_conf["pg_user"]+":"+pg_conf["pg_pw"]+"@"+pg_conf["pg_host"]+"/"+pg_conf["pg_database"]

engine = create_engine(
    DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


