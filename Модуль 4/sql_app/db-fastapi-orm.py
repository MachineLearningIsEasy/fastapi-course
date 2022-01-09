
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return "Phonebook"

@app.post("/add-user/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/get-user/", response_model=schemas.User)
def get_user(lastname: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_lastname(db, lastname=lastname)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user