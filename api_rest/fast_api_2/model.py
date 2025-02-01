from sqlalchemy import create_engine, Column, Integer, String
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import Item


# FastAPI app instance

# Database setup
DATABASE_URL = "sqlite:///./test.db"

# This line defines the database URL. 
# In this case, it's using SQLite, a lightweight disk-based database. 
# The ///./test.db part means the database file will be created in the current directory with the name "test.db"

engine = create_engine(DATABASE_URL)
# This creates a SQLAlchemy "engine", 
# which is the starting point for any SQLAlchemy application. 
# It's essentially the source of the database connection for all operations.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This creates a custom session factory. Sessions are used to manage database operations:
# autocommit=False: Transactions won't be automatically committed.
# autoflush=False: Changes won't be automatically flushed to the database.
# bind=engine: Associates this session with our database engine.

  
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#This defines a function named get_db. 
# db = SessionLocal()
# This creates a new SQLAlchemy Session instance using the SessionLocal factory we defined earlier. Each call to SessionLocal() creates a new session.
# try:
# This starts a try block to ensure proper handling of the session, even if errors occur.
# yield db
# This is the key part. Instead of returning the db session, it yields it. 
# This turns the function into a generator. When used as a dependency in FastAPI, this allows the session to be used for the duration of a request and then properly closed afterward.
# finally: 
# This block ensures that the following code runs whether an exception was raised or not.
# db.close()
# This closes the database session. It's crucial to always close sessions to return connections to the database pool, preventing resource leaks.

 
 
# Pydantic model for request data
"""Request data models are used to define the structure and validation rules for incoming data sent to the server, 
typically through HTTP requests (e.g., POST, PUT, PATCH)."""
class ItemCreate(BaseModel):
    name: str
    description: str
 
 
# Pydantic model for response data
"""Response data models, on the other hand, 
are used to define the structure of the data that the server sends back to the client in response to a request."""    
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str


