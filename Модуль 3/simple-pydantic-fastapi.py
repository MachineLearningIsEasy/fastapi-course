from fastapi import FastAPI
from typing import Optional
import pandas as pd
import json
from data_request_model import *


app = FastAPI()



@app.get("/")
async def root():
    return "Phonebook"


@app.post("/add-user")
async def add_user(parameters: User):
# Считываем/создаем телефонный справочник
    try:
        df_phonebook = pd.read_csv('db.csv')
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname','Lastname','Phone number','Age'])


    user_dict = {}
    print(type(parameters))

    user_dict['Firstname'] = parameters.firstname
    user_dict['Lastname'] = parameters.lastname
    user_dict['Phone number'] = parameters.phone_number
    
    print(f'Firstname: {parameters.firstname}')
    print(f'Lastname: {parameters.lastname}')
    print(f'Phone number: {parameters.phone_number}')
    if parameters.age:
        print(f'Age: {parameters.age}')
        user_dict['Age'] = parameters.age
    else:
        user_dict['Age'] = 0

    print(user_dict)
    df_temp = pd.DataFrame([user_dict])
    print(df_phonebook)
    print(df_temp)
    df_phonebook = pd.concat([df_phonebook,df_temp])
    df_phonebook.to_csv('db.csv', index=False)
    return 'user is added'


@app.get("/get-user")
async def get_user(lastname: str):
    try:
        df_phonebook = pd.read_csv('db.csv')
        # df_phonebook['Phone number'] = df_phonebook['Phone number'].astype(str) 
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname','Lastname','Phone number','Age'])

    df_temp = df_phonebook[df_phonebook['Lastname']==lastname]
    if df_temp.empty:
        return 'There is no such user'
    print(dict(df_temp.iloc[0]))
    return json.dumps(dict({'Phone number':df_temp.iloc[0]['Phone number']}))# "Jon Snow, 81992128787, 31"