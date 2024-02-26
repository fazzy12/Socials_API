from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from typing import Optional, List
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='socialsapi',
                                user='postgres',
                                password='virgin123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Created connection to database')
        break
    except Exception as e:
        print('Error: ', e)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
