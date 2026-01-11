from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "FastAPI with Python 3.12.7 OK"}
