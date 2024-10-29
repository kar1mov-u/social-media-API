from fastapi import FastAPI,HTTPException,Response,Depends,APIRouter
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from .. import models,schemas

router = APIRouter(
    prefix='/posts'
)

@router.get('',response_model=List[schemas.Post])
async def get_posts(db:Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts =cursor.fetchall()
    # print(type(posts))
    posts = db.query(models.Post).all()
    return posts



@router.post('/',status_code=201,response_model=schemas.Post)
async def create_post(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}',response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db) ):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return post


@router.delete('/{id}',status_code=204)
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
    

@router.put("/{id}",response_model=schemas.Post)
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
    
    return post_query.first()

