from pydantic import BaseModel
from typing import Optional

class ISBNRequest(BaseModel):
    isbn: str

class SaveRequest(BaseModel):
    b_title: str
    isbn: str
    price: Optional[str] = ""
    quantity: Optional[str] = ""
