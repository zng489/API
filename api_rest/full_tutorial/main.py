from fastapi import FastAPI
from typing import Optional 
from pydantic import BaseModel
import uvicorn
import requests
myapp = FastAPI()

@myapp.get('/')
def index ():
    return 'hey'


@myapp.get('/blog')
def index (limit : int=10, published : bool=True, sort: Optional[str] = None):
    # only get 10 published blogs
    # return published 
    if published:
        return {'data':f'{limit} published from the db'}
    else:
        return {'data':'BLOGS'}
    
# http://127.0.0.1:8000/blog?limit=800
# http://127.0.0.1:8000/blog?sort=latest

@myapp.get('/about')
def index ():
    return {'data':{'name':'Sarthak'}}

# Dynaminc routing
@myapp.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished'} 

# Dynaminc routing
@myapp.get('/blog/{id}')
def index (id: int):
    # fetch blog  with id = id
    return {'data':id}

#uvicorn main:myapp --reload

@myapp.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of blog with id = id
    return {'data':{'1', '2'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@myapp.post('/blog')
def create_blog(request: Blog):
    #return request
    return {'data':f'Blog is created {request.title}'}
            
@myapp.post('/blogs')
def create(title, body):
        #return request
    return {'data':f'Blog is created {requests.title}'}
            
            
            
# docs
# redoc

# https://www.youtube.com/watch?v=7t2alSnE2-I&ab_channel=Bitfumes
# 46:20
# 51:01
# 1:15:47

# if __name__ == "__main__":
    # uvicorn.run(myapp, host="127.0.0.1", port=10)
    # python main.py
# uvicorn main:app --reload