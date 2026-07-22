# to run the code -> uvicorn app.main:app --reload  
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, post, user , vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI() # instance of fast api
  
origins =["https://www.google.com"]

    # [
    #     "http://localhost:3000",
    #     "http://127.0.0.1:3000",
    # ]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/") # here get is just one of the HTTP method
async def root():
  return {"message" : "Hello Sahil"}  # fast api convert this into a json , whichis the universal for wev dev










