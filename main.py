from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

class Post(BaseModel):
  title : str
  content : str
  published : bool = True
  rating : int = 0

app = FastAPI() # instance of fast api

@app.get("/") # here get is just one of the HTTP method
async def root():
  return {"message" : "Hello Sahil"}  # fast api convert this into a json , whichis the universal for wev dev

@app.get("/post")
async def get_post():
  return {"post" : "this is yout post"}

@app.post("/createpost")
async def Create_Post(new_post : Post): # i used pydantic here , i mean its a kind of checkup on the recived data
  print(new_post.rating)
  return {"data" : "new post"}