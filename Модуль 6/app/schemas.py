from pydantic import BaseModel, validator, root_validator, ValidationError
from typing import List, Optional


class User(BaseModel):
    firstname: str
    lastname: str
    phone_number: str
    age: int
    class Config:
        orm_mode=True

class AuthModel(BaseModel):
    username: str
    password: str