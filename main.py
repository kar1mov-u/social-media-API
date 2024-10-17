from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published :bool = True
    rating : Optional[int] = None

@app.get('/')
async def root():
    return {"message":"welcome niggas"}



@app.get('/posts')
async def get_posts():
    return {"message":"All of your posts"}



@app.post('/createposts')
async def create_post(post:Post):
    n =post.model_dump()
    return {"data":n}