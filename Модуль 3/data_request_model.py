from pydantic import BaseModel, validator, root_validator
from typing import Optional


class User(BaseModel):
    firstname: str
    lastname: str
    phone_number: str
    age: Optional[int] = 0

    # @validator("phone_number")
    # def parse_phone_number(cls, phone_number: str):
    #     return f"Phone: {phone_number} XXX"

    # @validator("phone_number")
    # def parse_phone_number(cls, phone_number, values, **kwargs):
    #     print(values.keys())
    #     return phone_number

    @root_validator
    def parse_phone_number(cls, values):
        print(values.keys())
        return values