# to run the code -> uvicorn app.main:app --reload  
from fastapi import FastAPI , Response , status , HTTPException  , Depends # this time i included the header for catching exceptions
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import models , schemas
from .database import engine , SessionLocal , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



############## for the connection with the database on our local system through psycopg2
# while True:
#   try:
#     conn = psycopg2.connect(
#         host='localhost',
#         database='SOCIAL_MEDIA',
#         user='postgres',
#         password='1234',
#         cursor_factory=RealDictCursor    #with realdict cursor , we can access valuse by name ex-> id["sahil"]
#     )
#     cursor = conn.cursor()
#     print("Database Connected Successfully!")
#     break
#   except Exception as error:
#     print("Connection to DataBase Failed")
#     print("Error: ",error)
#     time.sleep(2)
  

app = FastAPI() # instance of fast api
  

@app.get("/") # here get is just one of the HTTP method
async def root():
  return {"message" : "Hello Sahil"}  # fast api convert this into a json , whichis the universal for wev dev

# now we using sql alchemy orm
@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)

    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.post_back)
async def Create_Post(post: schemas.Post_Create, db:Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.post_back)
async def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found"
        )

    return post
    
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT) # to delete the post with it's id , in modern way
async def delete_post(id: int , db:Session = Depends(get_db)):
  
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.delete(synchronize_session=False)
    if deleted_post ==0:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id:{id} not found to delete"
    )
      
    db.commit()
    # conn.commit()
    return 

@app.put("/posts/{id}", response_model=schemas.post_back)
async def update_post(id: int, updated_post: schemas.Post_Update, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found"
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    updated_post = post_query.first()

    return updated_post