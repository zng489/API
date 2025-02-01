from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from data_model_schema import get_db
from data_model_schema import User
from data_model_schema import UserCreate, UserUpdate



app = FastAPI()


@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()