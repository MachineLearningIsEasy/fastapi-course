from pydantic import BaseModel, validator, root_validator


class User(BaseModel):
    firstname: str
    lastname: str
    phone_number: str
    age: int
    
    class Config:
        orm_mode=True