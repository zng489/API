
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

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
    
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This creates a custom session factory. Sessions are used to manage database operations:
# autocommit=False: Transactions won't be automatically committed.
# autoflush=False: Changes won't be automatically flushed to the database.
# bind=engine: Associates this session with our database engine.

Base = declarative_base()
# This creates a base class for declarative class definitions. 
# You'll use this base class to define your database models (tables).

# Database model
class Item(Base):
    __tablename__ = "items"
    # __tablename__ = "items"
    # This special attribute tells SQLAlchemy what name to use for the table in the database. 
    # In this case, the table will be named "items".

    id = Column(Integer, primary_key=True, index=True)
    # id = Column(Integer, primary_key=True, index=True)
    # This line defines the id column of the table:
    # Integer: The data type of this column is an integer.
    # primary_key=True: This column is the primary key of the table.
    # index=True: An index will be created for this column, which can speed up queries.

    name = Column(String, index=True)
    description = Column(String)
    # Item.id
    # Item.name
    # Item.description 

# Create tables
Base.metadata.create_all(bind=engine)

# Base: This refers to the declarative base class we created earlier with declarative_base(). 
# It's the base class for all your model classes (like the Item class we just discussed).

# metadata: This is an object attached to your Base class that keeps track of all the models and tables that have been defined.

# create_all(): This is a method that instructs SQLAlchemy to create all tables that don't yet exist in the database. 
# It goes through all the models that inherit from Base and creates corresponding tables if they're not already present.

# bind=engine: This parameter tells the create_all() method which database engine to use when creating the tables. 
# It's using the engine we created earlier with create_engine().

# https://medium.com/juntos-somos-mais/fastapi-construindo-microsservi%C3%A7os-de-alta-performance-6f3063e13102
# https://github.com/izaguerreiro/fastapi_techtalk/blob/master/app/schemas.py
# https://github.com/izaguerreiro/fastapi_techtalk/blob/master/app/main.py