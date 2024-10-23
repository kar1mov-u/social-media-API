from fastapi import FastAPI,HTTPException,Response,Depends
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)



app = FastAPI()




class Post(BaseModel):
    title:str
    content:str
    published :bool = True


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


@app.get('/sqlalchemy')
def test_posts(db:Session=Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data":posts}


@app.get('/posts')
async def get_posts(db:Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts =cursor.fetchall()
    # print(type(posts))
    posts = db.query(models.Post).all()
    return {"message":posts}



@app.post('/posts',status_code=201)
async def create_post(post:Post,db:Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}


@app.get('/post/{id}')
def get_post(id:int ):
    cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return {"message":post}


@app.delete('/posts/{id}',status_code=204)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=404,detail="There is no such post")
    return Response(status_code=204)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title,post.content, post.published,str(id)))
    p = cursor.fetchone()
    conn.commit()
    if not p:
        raise HTTPException(status_code=404, detail="THere is no such post")

    return {"message":p}