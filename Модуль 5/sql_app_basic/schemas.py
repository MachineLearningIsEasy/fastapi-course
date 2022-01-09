from pydantic import BaseModel, validator, root_validator, ValidationError
from typing import List, Optional


class User(BaseModel):
    firstname: str
    lastname: str
    phone_number: str
    age: int
    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

class UserInDB(User):
    hashed_password: str