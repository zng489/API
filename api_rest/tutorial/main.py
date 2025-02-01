#import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import HTTPException

app = FastAPI()

fakeDatabase = {
    1: {"task":"Clean car"},
    2: {"task":"Write blog"},
    3: {"task":"Start stream"}
}

BANDS = [
    {"id":1, "name":"The Kinks", "genre":"Rock"},
    {"id":2, "name":"Aphex Twin", "genre":"Electronic"},
    {"id":3, "name":"Black Sabbath", "genre":"Metal",
     "albums":[{"title":"Master of Reality", "release_date":"1971-07-21"},
               ]},
    {"id":4, "name":"Wu-Tang Clan", "genre":"Hip-Hop"},
    ]


list_of_usernames = list()
# list_of_usernames = []

@app.get("/")
def get_user():
    return {"user": {"name": "Fulano","age": "30"}}


@app.get("/item")
def get_user():
    return ["Item 1", "Item 2", "Item 3"]

@app.get("/fakeDatabase")
def get_user():
    return fakeDatabase

@app.get("/{id}")
def get_user(id:int):
    return fakeDatabase[id]


@app.post("/")
def addItem(task:str):
    newId = len(fakeDatabase.keys()) + 1
    fakeDatabase[newId] = {"task":task}
    return fakeDatabase


@app.get("/home/{user_name}", description='Getting!!')
def write_home(user_name: str):
    return {
        "Name": user_name,
        "Age": 33
    }


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length = 1)

BOOKS = []


@app.put("/username/{user_name}")
def put_date(user_name: str):
    print(user_name)
    list_of_usernames.append(user_name)
    return {
        "username": user_name
    }

@app.post("/postData")
def post_data(user_name: str):
    list_of_usernames.append(user_name)
    return {
        "username": user_name
    }

@app.delete("/deleteData/{user_name}")
def delete_date(user_name: str):
    list_of_usernames.remove(user_name)
    return {
        "usernames":list_of_usernames
    }


@app.post("/")
def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise HTTPException (
        status_code=404,
        detail=f'ID {book_id} : Does not exist')

@app.delete('/{bookd_id}')
def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted'
    raise HTTPException(
        status_code = 404,
        detail = f'ID {book_id}: Does not exist'
    )

# https://www.youtube.com/watch?v=MCVcAAoDJS8&list=PLK8U0kF0E_D6l19LhOGWhVZ3sQ6ujJKq_