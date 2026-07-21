from sqlalchemy import create_engine # create_engine, it Creates the connection between SQLAlchemy and PostgreSQL.
from sqlalchemy.orm import sessionmaker, declarative_base # A sessionmaker'session is how SQLAlchemy talks to the database.
                                         # Allows you to create database tables using Python classes.
from .config import settings

SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')

engine = create_engine(SQLALCHEMY_DATABASE_URL) # responsible to connect to postgresql database 

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine # "Whenever you create a session, connect it using this engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
  