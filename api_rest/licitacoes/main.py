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

@app.post("/items", response_model=UserPost)
async def create_post(post: Item):
    tags_str = ",".join(post.tags)  # Convert list of tags to a comma-separated string
    query = post_table.insert().values(
        name=post.name,
        description=post.description,
        price=post.price,
        tax=post.tax,
        tags=tags_str  # Use the string representation of tags
    )
    last_record_id = await database.execute(query)
    return {**post.dict(), "id": last_record_id}

@app.get("/all", response_model=List[UserPost])
async def get_all_posts():
    query = post_table.select()
    result = await database.fetch_all(query)

    # Convert the result to a list of UserPost models
    posts = [
        UserPost(
            id=post['id'],
            name=post['name'],
            description=post['description'],
            price=post['price'],
            tax=post['tax'],
            tags=post['tags'].split(',') if post['tags'] else []
        )
        for post in result
    ]
    
    return posts

@app.get("/items/{item_id}", response_model=UserPost)
async def read_item(item_id: int):
    query = post_table.select().where(post_table.c.id == item_id)
    result = await database.fetch_one(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Convert the result to a UserPost model
    item = UserPost(
        id=result['id'],
        name=result['name'],
        description=result['description'],
        price=result['price'],
        tax=result['tax'],
        tags=result['tags'].split(',') if result['tags'] else []
    )

    return item

@app.put("/items/{item_id}", response_model=UserPost)
async def update_item(item_id: int, post_update: Item):
    # Check if the item exists
    existing_item = await database.fetch_one(post_table.select().where(post_table.c.id == item_id))
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the item with the new values
    tags_str = ",".join(post_update.tags)
    query = (
        post_table.update()
        .where(post_table.c.id == item_id)
        .values(
            name=post_update.name,
            description=post_update.description,
            price=post_update.price,
            tax=post_update.tax,
            tags=tags_str
        )
    )
    await database.execute(query)

    # Return the updated item
    updated_item = UserPost(
        id=item_id,
        name=post_update.name,
        description=post_update.description,
        price=post_update.price,
        tax=post_update.tax,
        tags=post_update.tags
    )
    return updated_item

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    # Check if the item exists
    existing_item = await database.fetch_one(post_table.select().where(post_table.c.id == item_id))
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Delete the item
    query = post_table.delete().where(post_table.c.id == item_id)
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
    
# https://python.plainenglish.io/integrating-payment-webhooks-with-fastapi-in-python-bd769961cafd