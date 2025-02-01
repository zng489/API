
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder 

# https://medium.com/juntos-somos-mais/fastapi-construindo-microsservi%C3%A7os-de-alta-performance-6f3063e13102
# https://github.com/izaguerreiro/fastapi_techtalk/blob/master/app/schemas.py
# https://github.com/izaguerreiro/fastapi_techtalk/blob/master/app/main.py
# FastAPI app instance

app = FastAPI()
 
# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
 
 
# Database model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
 
# Item.id
# Item.name
# Item.description 
 
# Create tables
Base.metadata.create_all(bind=engine)
 
 
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
# Pydantic model for request data
"""Request data models are used to define the structure and validation rules for incoming data sent to the server, typically through HTTP requests (e.g., POST, PUT, PATCH)."""
class ItemCreate(BaseModel):
    name: str
    description: str
 
 
# Pydantic model for response data
"""Response data models, on the other hand, are used to define the structure of the data that the server sends back to the client in response to a request."""    
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
 
 
# API endpoint to create an item
@app.post("/items/", response_model=ItemResponse)
# async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ItemResponse(**jsonable_encoder(db_item))
 
 
# API endpoint to read an item by ID
@app.get("/items/{item_id}", response_model=ItemResponse)
# async def read_item(item_id: int, db: Session = Depends(get_db)):
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = jsonable_encoder(db_item)
    return item_dict
 
 
# if __name__ == "__main__":
#    import uvicorn
 
#    # Run the FastAPI application using Uvicorn
#    uvicorn.run(app, host="127.0.0.1", port=8000)


'''
@app.delete("/delete/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
# Delete a single record
#user_to_delete = session.query(User).filter(User.id == 1).first()
#session.delete(user_to_delete)
#session.commit()

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from your_model_module import Item, ItemResponse, get_db
'''

@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    # Query the item to be deleted
    db_item = db.query(Item).filter(Item.id == item_id).first()

    # Check if the item exists
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Delete the item
    db.delete(db_item)
    db.commit()

    return db_item
