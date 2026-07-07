# to run the code -> uvicorn app.main:app --reload  
from fastapi import FastAPI , Response , status , HTTPException  , Depends# this time i included the header for catching exceptions
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import models
from .database import engine , SessionLocal , get_db
from sqlalchemy.orm import session

models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
  title : str
  content : str
  published : bool = True
  rating : int = 0

############## for the connection with the database on our local system
while True:
  try:
    conn = psycopg2.connect(
        host='localhost',
        database='SOCIAL_MEDIA',
        user='postgres',
        password='1234',
        cursor_factory=RealDictCursor    #with realdict cursor , we can access valuse by name ex-> id["sahil"]
    )
    cursor = conn.cursor()
    print("Database Connected Successfully!")
    break
  except Exception as error:
    print("Connection to DataBase Failed")
    print("Error: ",error)
    time.sleep(2)
  

app = FastAPI() # instance of fast api
  

@app.get("/") # here get is just one of the HTTP method
async def root():
  return {"message" : "Hello Sahil"}  # fast api convert this into a json , whichis the universal for wev dev

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM "POSTS" """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def Create_Post(post: Post):
    cursor.execute("""INSERT INTO "POSTS"(title , content , published) VALUES(%s,%s,%s) RETURNING *""",(post.title , post.content , post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/latest") # to check the latest appended post
async def get_latest_post():
  post =  my_posts[len(my_posts)-1]
  return {"details": post}

@app.get("/posts/{id}")
async def get_post(id: int):

    cursor.execute("""SELECT * FROM "POSTS" WHERE id = %s""",(id,))
    post = cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found" 
        )

    return {"post_detail": post}
    
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT) # to delete the post with it's id , in modern way
async def delete_post(id: int):
  
    cursor.execute("""DELETE FROM "POSTS" WHERE id = %s RETURNING *""",(id,))
    deleted_post = cursor.fetchone()
    
    if deleted_post is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id:{id} not found to delete"
    )
      
    conn.commit()
    return 

@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post):

    cursor.execute(
        """
        UPDATE "POSTS"
        SET title = %s,
            content = %s,
            published = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            updated_post.title,
            updated_post.content,
            updated_post.published,
            id
        )
    )

    post = cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found"
        )

    conn.commit()

    return {
        "message": "Post updated",
        "post": post
    }