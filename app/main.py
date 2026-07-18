# to run the code -> uvicorn app.main:app --reload  
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI() # instance of fast api
  
@app.get("/") # here get is just one of the HTTP method
async def root():
  return {"message" : "Hello Sahil"}  # fast api convert this into a json , whichis the universal for wev dev

app.include_router(post.router)
app.include_router(user.router)