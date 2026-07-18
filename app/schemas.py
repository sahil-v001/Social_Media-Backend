from pydantic import BaseModel
from datetime import datetime

class Post_Create(BaseModel):
  title : str
  content : str
  published : bool = True
  
class post_back(BaseModel):
  title : str
  content : str
  published : bool = True
  
# class Post_Update(BaseModel):
#   published : bool
  
class Post_Update(Post_Create):
  published : bool
  
class config:
  orm_mode = True
  
  