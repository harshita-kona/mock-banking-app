from sqlalchemy.orm import Session
from uuid import uuid4
from . import models, schemas


def create_user_account(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "nothashed"
    db_user = models.Users(user_id= str(uuid4()), email_id=user.email_id, first_name= user.first_name, middle_name= user.middle_name, last_name= user.last_name, date_of_birth= user.date_of_birth, occupation= user.occupation, mobile_no= user.mobile_no, created_date= user.created_date, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
