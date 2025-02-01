from typing import Any, List, Union
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import bcrypt

###########################################################################################
# MAIN.py AUTHENTICATION ##################################################################
###########################################################################################

from fastapi import FastAPI, status, Depends, HTTPException
import models
from database import engine, SessionLocal
from fastapi.routing import Annotated
from sqlalchemy.orm import Session
import auth
from auth import get_current_user

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
user_dependency = Annotated[dict, Depends(get_current_user)]

#@app.get("/", status_code=status.HTTP_200_OK)
#async def user(user:None, db:db_dependency):
#    if user is None:
#        raise HTTPException(status_code=401, detail='Authentication Failed')
#    return {"User":user}


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User":user}



# https://www.youtube.com/watch?v=0A_GCXBCNUQ
# 16:22
# https://www.youtube.com/watch?v=7t2alSnE2-I

# 19:24


