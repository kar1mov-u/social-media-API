from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published :bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    
        
class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserReturn(BaseModel):
    id:int
    email:str
    created_at:datetime
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str