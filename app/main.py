from fastapi import FastAPI,HTTPException,Response,Depends
import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor
import time
from .utils import hash_password
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db
from .routers import post,user,auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)



while True:
    try:
        conn = psycopg2.connect(host ='localhost',database = 'fastapi',user = 'postgres', password = 'karimov1', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was sucessful")
        break
    except Exception as er:
        print("Connection to database failed")
        print(f"Error: {er}")
        time.sleep(2)
    
    
@app.get('/')
async def root():
    return {"message":"welcome niggas"}


