from fastapi import FastAPI , Response , status , HTTPException # this time i included the header for catching exceptions
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
  raise HTTPException(status_code=status.HTTP_201_CREATED,
                      detail=post_dict)

@app.get("/posts/latest") # to check the latest appended post
async def get_latest_post():
  post =  my_posts[len(my_posts)-1]
  return {"details": post}

@app.get("/posts/{id}")
async def get_post(id: int , response : Response):   # we can remove this exception  , because we used the HTTP exception , which do the same work in one line
    for post in my_posts:
        if post["id"] == id:
          return {"post_detail": post}
     
   # response.status_code = status.HTTP_404_NOT_FOUND
   # return {"message": f"Post with id:{id} was not found"}
   
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                       detail=f"post with id:{id} wan not found")
    

@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT) # to delete the post with it's id , in modern way
async def delete_post(id: int):

    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post) # we keep the return empty , because 204 is literaly return nothing
            return 

    raise HTTPException(   #used it when we are like want to raise querry where there is an error
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id:{id} not found to delete"
    )   
    
    
@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post):

    for post in my_posts:
        if post["id"] == id:

            post["title"] = updated_post.title
            post["content"] = updated_post.content

            return {
                "message": "Post updated",
                "post": post
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id:{id} was not found"
    )