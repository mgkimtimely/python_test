from typing import Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "안녕븅시낭"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> dict[str, Union[int, str, None]]:
    """
    - item_id: int 타입으로 받는 Path Parameter
    - q: Optional[str] 타입으로 받는 Query Parameter
    - 반환값: dict[str, Union[int, str, None]]로 명시
    """
    return {"item_id": item_id, "q": q}