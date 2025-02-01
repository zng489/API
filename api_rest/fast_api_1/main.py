from fastapi import FastAPI
from typing import Optional 
from pydantic import BaseModel
import uvicorn
import requests
from database import Item
from model import ItemCreate, ItemResponse,  get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session

from fastapi.encoders import jsonable_encoder 


myapp = FastAPI()

@myapp.get('/')
def index ():
    return 'Response body /'

@myapp.get('/n_1')
def index (limit : int=10,
           published : bool=True,
           sort: Optional[str] = None):
    # only get 10 published blogs
    # return published 
    if published:
        # limit: 1000
        # published: False
        # sort: None
        return {"data:f'{limit} {published} {sort} published from the db"}
    else:
        # limit: 1000
        # published: False
        # sort: Fulano
        return {'data':'BLOGS'}

@myapp.get('/n_2')
def index ():
    return {'data':{'name':'Sarthak'}}

# Dynaminc routing
@myapp.get('/n_3/unpublished')
def unpublished():
    return {'data':'all unpublished'} 

@myapp.get('/n_4/{id}')
def index (id: int):
    # fetch blog  with id = id
    return {'data':id}

@myapp.get('/n_5/{id}/comments')
def comments(id):
    # fetch comments of blog with id = id
    return {'data':{'1', '2', id }}


# API endpoint to create an item
@myapp.post("/items/", response_model=ItemResponse)
# async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ItemResponse(**jsonable_encoder(db_item))
 
 
# API endpoint to read an item by ID
@myapp.get("/items/{item_id}", response_model=ItemResponse)
# async def read_item(item_id: int, db: Session = Depends(get_db)):
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = jsonable_encoder(db_item)
    return item_dict








#uvicorn main:myapp --reload