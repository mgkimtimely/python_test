from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from requests import Session
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class ItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

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