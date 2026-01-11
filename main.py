# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="TechNotesPark API", version="1.0")

# -----------------------
# Pydantic 모델 정의
# -----------------------
class Item(BaseModel):
    name: str = Field(..., example="Laptop")           # Swagger UI에 예시값 표시
    price: float = Field(..., example=1200.50)
    description: str | None = Field(None, example="FastAPI Notebook")

# -----------------------
# 루트 경로
# -----------------------
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# -----------------------
# GET 경로 파라미터 예제
# -----------------------
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}

# -----------------------
# POST 요청 예제
# -----------------------
@app.post("/items/")
def create_item(item: Item):
    """
    POST /items/
    Body 예시: Swagger UI에 자동 표시
    """
    return {"message": "Item received", "item": item}
