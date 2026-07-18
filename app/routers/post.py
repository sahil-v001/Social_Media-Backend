from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

# Router for all post-related APIs
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Here we are using SQLAlchemy ORM to fetch all posts.
@router.get("/", response_model=list[schemas.post_back])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts


# Create a new post.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.post_back)
def create_post(post: schemas.Post_Create, db: Session = Depends(get_db)):

    # Convert the Pydantic model into a SQLAlchemy model.
    new_post = models.Post(**post.model_dump())

    # Save the post to the database.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get a particular post using its ID.
@router.get("/{id}", response_model=schemas.post_back)
def get_post(id: int, db: Session = Depends(get_db)):

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
def delete_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = post_query.delete(synchronize_session=False)

    # If no post was deleted, return a 404 response.
    if deleted_post == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found to delete"
        )

    db.commit()

    return


# Update a post using its ID.
@router.put("/{id}", response_model=schemas.post_back)
def update_post(
    id: int,
    updated_post: schemas.Post_Update,
    db: Session = Depends(get_db)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Check whether the post exists.
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    # Update the post with the new values.
    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()