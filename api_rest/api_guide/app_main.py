from typing import Any, List, Union
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import bcrypt
###########################################################################################
# This setup provides the foundation for interacting with the SQLite database in a Python #
# Could come from an env var ##############################################################
###########################################################################################

DATABASE_URL = "sqlite:///data.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

######################################################################################### 
# Creating Table name ###################################################################
#########################################################################################

table_one = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("cod", sqlalchemy.String))


######################################################################################### 
# Creating Ref Table name ###############################################################
#########################################################################################

ref_table = sqlalchemy.Table(
    "ref",
    metadata,
    sqlalchemy.Column("id_ref", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body_ref", sqlalchemy.String),
    sqlalchemy.Column("description_ref", sqlalchemy.ForeignKey("posts.id"), nullable=False)
)


engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
app = FastAPI()


######################################################################################### 
# Creating Ref Table name ###############################################################
#########################################################################################

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    cod: str


# What return when the API is used
class UserPost(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None
    cod: str

###########################################################################################
# CRUD #################################################################################### 
###########################################################################################

@app.post("/items", response_model=UserPost)
async def create_post(post: Item):
    #tags_str = ",".join(post.tags)  # Convert list of tags to a comma-separated string
    query = table_one.insert().values(
        name=post.name,
        description=post.description,
        cod=post.cod # Use the string representation of tags
    )
    last_record_id = await database.execute(query)
    return {**post.dict(), "id": last_record_id}

"""
For example, 
if post.dict() returns {"name": "Example", "description": "This is an example"}, 
then **post.dict() effectively becomes name="Example", 
description="This is an example" when passed as arguments to a function.
"""

@app.get("/all", response_model=List[UserPost])
async def get_all_posts():
    query = table_one.select()
    result = await database.fetch_all(query)
    # Convert the result to a list of UserPost models
    posts = [
        UserPost(
            id=post['id'],
            name=post['name'],
            description=post['description'],
            cod=post['cod']
        )
        for post in result
    ]
    return posts

@app.get("/items/{item_id}", response_model=UserPost)
async def read_item(item_id: int):
    query = table_one.select().where(table_one.c.id == item_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # Convert the result to a UserPost model
    item = UserPost(
        id=result['id'],
        name=result['name'],
        description=result['description'],
        cod=result['cod']
    )
    return item


@app.put("/items/{item_id}", response_model=UserPost)
async def update_item(item_id: int, post_update: Item):
    # Check if the item exists
    existing_item = await database.fetch_one(table_one.select().where(table_one.c.id == item_id))
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the item with the new values
    query = (
        table_one.update()
        .where(table_one.c.id == item_id)
        .values(
            name=post_update.name,
            description=post_update.description,
            cod=post_update.cod)
    )
    await database.execute(query)

    # Return the updated item
    updated_item = UserPost(
        id=item_id,
        name=post_update.name,
        description=post_update.description,
        cod=post_update.cod
    )
    return updated_item



@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    # Check if the item exists
    existing_item = await database.fetch_one(table_one.select().where(table_one.c.id == item_id))
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # Delete the item
    query = table_one.delete().where(table_one.c.id == item_id)
    await database.execute(query)

    # Return a response indicating successful deletion
    return {"message": "Item deleted successfully"}




class WebhookPayload(BaseModel):
    event: str
    data: dict

@app.post("/webhook")
async def webhook_handler(payload: WebhookPayload):
    """
    Webhook handler endpoint.

    This endpoint expects a JSON payload with an "event" and "data" field.
    """
    try:
        # Process the webhook payload
        event = payload.event
        data = payload.data

        # Your webhook processing logic goes here
        print(f"Received webhook for event '{event}': {data}")

        # You can add your own business logic or integrations here

        return {"message": "Webhook received successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

###########################################################################################
# MAIN.py AUTHENTICATION ##########################################################################
###########################################################################################
'''
from fastapi import FastAPI, status, Depends, HTTPException
import models
from database import engine, SessionLocal
from fastapi.routing import Annotated
from sqlalchemy.orm import Session
import auth


app = FastAPI()
app.include_router(auth.router)


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user:None, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User":user}
'''
    
# https://www.youtube.com/watch?v=0A_GCXBCNUQ
# 16:22