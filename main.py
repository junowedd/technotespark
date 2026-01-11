# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="TechNotesPark API", version="1.0")

# 루트 경로
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# 경로 파라미터 예제
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}

# POST 요청 예제 (JSON 데이터 받기)
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item received", "item": item}
