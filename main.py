from fastapi import FastAPI

app = FastAPI()

@app.get("/debug")
def root():
    x = 10   # ← 여기에 breakpoint 걸기
    y = x * 2
    return {"status": "FastAPI with Python 3.12.7 OK"}
