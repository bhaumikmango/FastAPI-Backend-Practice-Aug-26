from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

while True:    
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'password123', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('DB connection successful')
        break
    except Exception as e:
        print(e)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)