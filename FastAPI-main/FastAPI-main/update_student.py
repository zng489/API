from pydantic import BaseModel
from typing import Optional


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int]= None
    year: Optional[str] = None