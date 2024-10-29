from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models
from ..utils import check_password
router = APIRouter(tags = ['Authentication'])

@router.post('/login')
def login(user_creds:schemas.UserLogin, db:Session=Depends(get_db)):
    
    user=db.query(models.User).filter(models.User.email==user_creds.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not check_password(user_creds.password,user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    #Create and return JWT token
    
    return {"token":"example token"}
        
    