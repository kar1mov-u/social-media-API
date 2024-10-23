from fastapi import FastAPI,HTTPException,Response
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
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
    
    
my_posts= [{"title":"My Post", "content":"Content of my Post", "published":False, "rating":10, "id":1}]

def find_post(id):
    for post in my_posts:
        if post['id']==id:
            return post

@app.get('/')
async def root():
    return {"message":"welcome niggas"}



@app.get('/posts')
async def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts =cursor.fetchall()
    print(type(posts))
    return {"message":posts}



@app.post('/posts',status_code=201)
async def create_post(post:Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
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