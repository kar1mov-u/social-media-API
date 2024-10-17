from fastapi import FastAPI,HTTPException,Response
from typing import Optional
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published :bool = True
    rating : Optional[int] = None

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
    return {"message":my_posts}



@app.post('/posts',status_code=201)
async def create_post(post:Post):
    n =post.model_dump()
    r_id = randrange(0,10000)
    n["id"]=r_id
    my_posts.append(n)
    return {"data":n}

@app.get('/post/{id}')
def get_post(id:int ):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return {"message":post}

@app.delete('/posts/{id}',status_code=204)
def delete_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404,detail="There is no such post")
    my_posts.remove(post)
    return Response(status_code=204)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    post_dic = post.model_dump()
    p = find_post(id)
    if not p:
        raise HTTPException(status_code=404, detail="THere is no such post")
    ind = my_posts.index(p)
    post_dic['id']=id
    my_posts[ind]=post_dic
    return {"message":"Updated Post"}