from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
async def root():
    return "Phonebook"


@app.post("/add-user")
async def add_user(firstname: str, lastname: str, phone_number: str, age: Optional[int] = None):
    print(f'Firstname: {firstname}')
    print(f'Lastname: {lastname}')
    print(f'Phone number: {phone_number}')
    if age:
        print(f'Age: {age}')

    return 'user is added'


@app.get("/get-user")
async def get_user(lastname: str):
    return "Jon Snow, 81992128787, 31"