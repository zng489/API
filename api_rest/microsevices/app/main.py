import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/address_/{cep}")
async def search_address_by_cep(cep: str):
    response = requests.get(f"http://viacep.com.br/ws/{cep}/json/")
    return response.json() 


@app.get("/address/{cep}")
async def search_address_by_cep(cep: str = Path(default=Any, max_length=8, min_length=8)):
    response = requests.get(f"http://viacep.com.br/ws/{cep}/json/")
    return response.json()