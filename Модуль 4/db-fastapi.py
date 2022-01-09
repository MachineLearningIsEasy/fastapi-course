from fastapi import FastAPI
from typing import Optional
import pandas as pd
import json
from schemas import *
import psycopg2


app = FastAPI()


HOST_DB = '0.0.0.0'
PORT = 5432
POSTGRES_USER='unicorn_user'
POSTGRES_PASSWORD='magical_password'
POSTGRES_DB='rainbow_database'



@app.get("/")
async def root():
    return "Phonebook"

@app.post("/add-user")
async def add_user(parameters: User):
    # создаем коннектор
    conn = psycopg2.connect(host=HOST_DB, port = 5432, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
    # создаем курсор
    cur = conn.cursor()

    # выполняем SQL запрос
    cur.execute("INSERT INTO phonebook (firstname, lastname, phone_number, age) VALUES(%s, %s, %s,%s)", (parameters.firstname, parameters.lastname, parameters.phone_number, parameters.age))
    
    # все коммитим и закрываем
    conn.commit()
    conn.close()
    cur.close()
    return 'user is added'



@app.get("/get-user")
async def get_user(lastname: str):
    # создаем коннектор
    conn = psycopg2.connect(host=HOST_DB, port = 5432, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
    df = pd.read_sql(f"select * from phonebook where lastname='{lastname}'", con=conn)
    if df.empty:
        return 'There is no such user'
    return json.dumps(df.iloc[0]['phone_number'])# "Jon Snow, 81992128787, 31"