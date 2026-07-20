from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas ,oauth2
from ..database import get_db

# Router for all post-related APIs
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Here we are using SQLAlchemy ORM to fetch all posts.
@router.get("/", response_model=list[schemas.post_back])
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()

    return posts


# Create a new post.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.post_back)
def create_post(post: schemas.Post_Create, db: Session = Depends(get_db) , current_user: int= Depends(oauth2.get_current_user)):

    # Convert the Pydantic model into a SQLAlchemy model.
    new_post = models.Post(user_id=current_user.id,**post.model_dump())

    # Save the post to the database.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get a particular post using its ID.
@router.get("/{id}", response_model=schemas.post_back)
def get_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # If the post doesn't exist, return a 404 response.
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    return post


# Delete a post using its ID.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return


# Update a post using its ID.
@router.put("/{id}", response_model=schemas.post_back)
def update_post(
    id: int,
    updated_post: schemas.Post_Update,
    db: Session = Depends(get_db),
    current_user: int= Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Check whether the post exists.
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
        
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    # Update the post with the new values.
    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()