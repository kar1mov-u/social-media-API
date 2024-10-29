from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas
from ..utils import hash_password
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/users'
)

@router.post("/",status_code=201,response_model=schemas.UserReturn)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    
    user.password = hash_password(user.password)
    
    new_user = models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400,detail = "Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    

@router.get('/{id}',response_model=schemas.UserReturn)
def get_user(id:int,db:Session=Depends(get_db)):
   user= db.query(models.User).filter(models.User.id==id).first()
   
   if not user:
       raise HTTPException(status_code=404, detail = f"User with id {id} does not exist")
   
   return user