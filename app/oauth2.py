from jose import JWTError, jwt
from datetime import datetime , timedelta
from .import schemas

SECRET_KEY = "3456f2tgf/24-*+d9f+g25fder54*+8*5*g1m,2gt9"
ALGORITHM =  "HS256"
EXPIRY_OF_TOKEN = 30    

def create_access_token(data:dict):
  to_encode = data.copy();
  expiry = datetime.now() + timedelta(minutes=EXPIRY_OF_TOKEN)
  
  to_encode.update({"exp":expiry})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


  