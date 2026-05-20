from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
  title : str
  content : str
  published : bool = True
  rating : int = 0

app = FastAPI() # instance of fast api

#i am trying the hardcoded version of saving post in memory instead of a database yet
my_posts = [{"titel":"title of post 1",
             "content":"content of post 1",
             "id":1},
            {"title":"title of post 2",
             "content":"content of post 2",
             "id":2}]

@app.get("/") # here get is just one of the HTTP method
async def root():
  return {"message" : "Hello Sahil"}  # fast api convert this into a json , whichis the universal for wev dev

@app.get("/posts")
async def get_post():
  return {"data" : my_posts}

@app.post("/posts")
async def Create_Post(post : Post): # i used pydantic here , i mean its a kind of checkup on the recived data
  post_dict = post.model_dump();
  post_dict["id"] = randrange(0,1000000)
  my_posts.append(post_dict)
  return {"data" : post_dict}