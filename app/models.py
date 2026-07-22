from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String , nullable=False)
    published = Column(Boolean,server_default=text("true"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

# here we made a new table user
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer ,primary_key=True, nullable=False)
    email = Column(String , unique=True , nullable=False)
    password = Column(String , nullable=False)
    age = Column(Integer , nullable=True )
    created_at = Column(TIMESTAMP(timezone=True), server_default= func.now(),nullable=False)
    

class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer , ForeignKey("users.id",ondelete="CASCADE" ), primary_key=True)
    post_id = Column(Integer , ForeignKey("posts.id",ondelete="CASCADE") , primary_key=True)