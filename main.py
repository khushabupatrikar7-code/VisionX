from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Vision X backend is alive"}