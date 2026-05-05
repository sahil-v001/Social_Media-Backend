from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI() 

@app.get("/")
async def root():
  return {"message" : "Hello Sahil"}  

@app.get("/post")
async def get_post():
  return {"post" : "this is yout post"}

@app.post("/createpost")
async def Create_Post(payload: dict = Body(...)):
  print(payload)
  return {"post created" : f" title : {payload['title']} , content : {payload['content']}"}