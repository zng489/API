from fastapi import FastAPI
from typing import Union
from typing import Optional 
from pydantic import BaseModel
import uvicorn

app_fast = FastAPI()

@app_fast.get("/")
def index():
    return {"name":"First Data"}

# Query Parameters FAST API
@app_fast.get('/blog')
def index (limit : int=50, published : bool=False, sort: Optional[str] = None):
    # only get 10 published blogs
    # return published 
    if published:
        return {'data':f'{limit} published from the db'}
    else:
        return {'data':'BLOGS'}
    

@app_fast.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
# http://127.0.0.1:8000/users/1/items/2?q=test,tex,asdasda,asdasdasda,asdasdas123123123,asd12312


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app_fast.post('/blog')
def create_blog(request: Blog):
    #return request
    return {'data':f'Blog is created {request.title}'}
            
#@myapp.post('/blogs')
#def create(title, body):
#        #return request
#    return {'data':f'Blog is created {request.title}'}

@app_fast.post('/blogs')
def create(title, body):
        #return request
    return {'data':f'Blog is created {request.title}'}
            