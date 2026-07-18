from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

# Router for all user-related APIs
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Here we are creating user data.
# This file will contain all CRUD operations related to users.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_check)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check if a user with the same email already exists.
    em = db.query(models.User).filter(models.User.email == user.email).first()

    if em:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already present"
        )

    # Hash the password before storing it in the database.
    utils.hashed(user)

    # Convert the Pydantic model into a SQLAlchemy model.
    new_user = models.User(**user.model_dump())

    # Save the new user to the database.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get a particular user using their ID.
@router.get("/{id}", response_model=schemas.User_check)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    # If the user doesn't exist, return a 404 response.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    return user


# Get all users from the database.
@router.get("/", response_model=list[schemas.User_check])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users