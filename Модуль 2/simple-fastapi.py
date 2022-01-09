from fastapi import FastAPI
from typing import Optional
import pandas as pd
import json

app = FastAPI()



@app.get("/")
async def root():
    return "Phonebook"


@app.post("/add-user")
async def add_user(firstname: str, lastname: str, phone_number: str, age: Optional[int] = None):
# Считываем/создаем телефонный справочник
    try:
        df_phonebook = pd.read_csv('db.csv')
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname','Lastname','Phone number','Age'])
        df_phonebook['Phone number'] = df_phonebook['Phone number'].astype(str) 


    user_dict = {}
    user_dict['Firstname'] = firstname
    user_dict['Lastname'] = lastname
    user_dict['Phone number'] = phone_number
    
    print(f'Firstname: {firstname}')
    print(f'Lastname: {lastname}')
    print(f'Phone number: {phone_number}')
    if age:
        print(f'Age: {age}')
        user_dict['Age'] = age
    else:
        user_dict['Age'] = 'None'

    print(user_dict)
    df_temp = pd.DataFrame([user_dict])
    print(df_phonebook)
    print(df_temp)
    df_phonebook = pd.concat([df_phonebook,df_temp])
    df_phonebook.to_csv('db.csv')
    return 'user is added'


@app.get("/get-user")
async def get_user(lastname: str):
    try:
        df_phonebook = pd.read_csv('db.csv')
        df_phonebook['Phone number'] = df_phonebook['Phone number'].astype(str) 
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname','Lastname','Phone number','Age'])

    df_temp = df_phonebook[df_phonebook['Lastname']==lastname]
    if df_temp.empty:
        return 'There is no such user'
    print(dict(df_temp.iloc[0]))
    return json.dumps(dict({'Phone number':df_temp.iloc[0]['Phone number']}))# "Jon Snow, 81992128787, 31"