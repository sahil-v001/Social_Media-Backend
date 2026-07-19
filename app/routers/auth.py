from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # at the place of manually configured schema , we are using the inbuilt library for this work

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login" , response_model=schemas.token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.check(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    #verify_token = oauth2.verify_access_token(access_token , user)
    
    return {"access_token" : access_token, "token_type": "bearer"}
  