#import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID


class Package( BaseModel):
    name: str
    number: str
    description: Optional[str] = None

app = FastAPI()

@app.get('/')
def hello_world():
    return 
