from fastapi import FastAPI,HTTPException,Response,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)



app = FastAPI()






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




@app.get('/posts')
async def get_posts(db:Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts =cursor.fetchall()
    # print(type(posts))
    posts = db.query(models.Post).all()
    return {"message":posts}



@app.post('/posts',status_code=201)
async def create_post(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}


@app.get('/post/{id}')
def get_post(id:int,db:Session=Depends(get_db) ):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return {"message":post}


@app.delete('/posts/{id}',status_code=204)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=404,detail="There is no such post")
    db.delete(post)
    db.commit()
    return Response(status_code=204)
    

@app.put("/posts/{id}")
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db) ):
    # cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title,post.content, post.published,str(id)))
    # p = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    old_post = post_query.first()
    if not old_post:
        raise HTTPException(status_code=404, detail="THere is no such post")
    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()
    
    return {"message":post_query.first()}