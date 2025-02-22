from pydantic import BaseModel
from typing import Optional


class AddressInput(BaseModel):
    cep: str
    logradouro: str
    complemento: Optional[str] = None
    bairro: str
    localidade: str
    uf: str
    ibge: int
    gia: int
    ddd: int