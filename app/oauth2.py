from jose import JWTError, jwt
from datetime import datetime , timedelta
from .import schemas
from fastapi import status , Depends , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .import database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "3456f2tgf/24-*+d9f+g25fder54*+8*5*g1m,2gt9"
ALGORITHM =  "HS256"
EXPIRY_OF_TOKEN = 30    

def create_access_token(data:dict):
  to_encode = data.copy();
  expiry = datetime.utcnow() + timedelta(minutes=EXPIRY_OF_TOKEN)
  
  to_encode.update({"exp":expiry})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def verify_access_token(token: str , credentials_exception):
  
  try:
    payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
    id: str = payload.get("user_id")
    
    if id is None:
      raise credentials_exception
    token_data = schemas.token_data(id=id)
    
  except JWTError as e:
    raise credentials_exception
  
  return token_data
  
def get_current_user(token:str= Depends(oauth2_scheme) , db: Session = Depends(database.get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate crendentials", headers={"WWW-Authenticate": "Bearer"})
  
  return verify_access_token(token,credentials_exception)
  
  
  