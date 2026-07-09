# to run the code -> uvicorn app.main:app --reload  
from fastapi import FastAPI , Response , status , HTTPException  , Depends # this time i included the header for catching exceptions
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import models
from .database import engine , SessionLocal , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
  title : str
  content : str
  published : bool = True

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

# now we using sql alchemy orm
@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
# here i used psycopg2
# def get_post():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def Create_Post(post: Post, db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title , content , published) VALUES(%s,%s,%s) RETURNING *""",(post.title , post.content , post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title  = post.title, content = post.content , published = post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}


@app.get("/posts/{id}")
async def get_post(id: int, db:Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id==id).first() # .first returns the post object , not the query anymore
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found" 
        )
    print(post)
    return {"post_detail": post}
    
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT) # to delete the post with it's id , in modern way
async def delete_post(id: int , db:Session = Depends(get_db)):
  
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    
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

@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post , db:Session = Depends(get_db)):

    # cursor.execute(
    #     """
    #     UPDATE posts
    #     SET title = %s,
    #         content = %s,
    #         published = %s
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (
    #         updated_post.title,
    #         updated_post.content,
    #         updated_post.published,
    #         id
    #     )
    # )

    # post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.update(updated_post.model_dump(),synchronize_session = False)

    if post == 0 :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found"
        )

    # conn.commit()
    db.commit()
    return {
        "message": "Post updated",
        "post": post
    }