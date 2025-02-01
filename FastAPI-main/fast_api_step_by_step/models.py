# https://teclado.com/fastapi-for-beginners/connect-fastapi-to-sql-database/
# https://teclado.com/fastapi-for-beginners/users-relationships-fastapi/

from typing import Any, List, Union
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = "sqlite:///data.db"  # could come from an env var
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# post_table IS NAME OF TABLE

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.String),
    sqlalchemy.Column("tax", sqlalchemy.String),
    sqlalchemy.Column("tags", sqlalchemy.String)
)

ref_table = sqlalchemy.Table(
    "posts_ref",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.ForeignKey("posts.id"), nullable=False)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: str
    tax: Union[str, None] = None
    tags: List[str] = []

# What return
class UserPost(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None
    price: str
    tax: Union[str, None] = None
    tags: List[str] = []