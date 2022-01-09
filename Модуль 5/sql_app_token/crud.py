from sqlalchemy.orm import Session

import models, schemas



def get_user_by_lastname(db: Session, lastname: str):
    return db.query(models.User_DB).filter(models.User_DB.lastname == lastname).first()



def create_user(db: Session, user: schemas.User):
    db_user = models.User_DB(firstname=user.firstname, lastname=user.lastname, phone_number=user.phone_number, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user