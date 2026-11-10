from fastapi import FastAPI
from app.routers import router

app = FastAPI()

app.include_router(router)

@app.get("/status")
def get_status():
    return{"status": "OK"}