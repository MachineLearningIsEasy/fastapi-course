import sys, os
import secrets
from auth import Auth
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, FastAPI, HTTPException, status, Security
from sqlalchemy.orm import Session
from deta import Deta
import crud, models, schemas
from database import SessionLocal, engine
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()
auth_handler = Auth()

deta = Deta('c049ac2i_h8qbgw1xcZBK9iUHKnXg8eTAWnwGyMtq')
users_db = deta.Base('users')


@app.post('/signup')
def signup(user_details: schemas.AuthModel):
    if users_db.get(user_details.username) != None:
        return 'Account already exists'
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        user = {'key': user_details.username, 'password': hashed_password}
        return users_db.put(user)
    except:
        error_msg = 'Failed to signup user'
        return error_msg

@app.post('/login')
def login(user_details: schemas.AuthModel):
    user = users_db.get(user_details.username)
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid username')
    if (not auth_handler.verify_password(user_details.password, user['password'])):
        return HTTPException(status_code=401, detail='Invalid password')
    access_token = auth_handler.encode_token(user['key'])
    refresh_token = auth_handler.encode_refresh_token(user['key'])
    return {'access_token': access_token, 'refresh_token': refresh_token}


@app.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}


@app.get("/")
async def root():
    return "Phonebook"

@app.post("/add-user/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return crud.create_user(db=db, user=user)
    return 'Invalid token'

@app.get("/get-user/", response_model=schemas.User)
def get_user(lastname: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_lastname(db, lastname=lastname)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user