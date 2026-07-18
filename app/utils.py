from passlib.context import CryptContext
from .import schemas 
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

def hashed(user):
  hashed_password = pwd_context.hash(user.password)
  user.password = hashed_password