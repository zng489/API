from typing import Union

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing_extensions import Annotated
from model import User

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#@app.get("/items/")
#async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#    return {"token": token}

@app.get("/items/")
def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


#async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#    user = fake_decode_token(token)
#    return user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user