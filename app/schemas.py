from pydantic import BaseModel, ConfigDict , EmailStr, Field
from datetime import datetime
from typing import Optional

class Post_Create(BaseModel):
    title: str
    content: str
    published: bool = True

class Post_Update(Post_Create):
    published: bool
# here we made the user schema 
class UserCreate(BaseModel):
  password: str = Field(min_length=8, max_length=72)
  email : EmailStr
  
# here we using it as pydantic , to check id the required things are correct or not
class User_check(BaseModel):
    id : int 
    email : EmailStr
    # password : str
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)

class User_Cred(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)
    
class token(BaseModel):
    access_token : str
    token_type : str
   
class token_data(BaseModel):
    id:Optional[int]= None
    
class post_back(Post_Create):
    id: int
    created_at: datetime
    user_id : int
    owner : User_check  

    model_config = ConfigDict(from_attributes=True)
