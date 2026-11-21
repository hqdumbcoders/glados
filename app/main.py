from fastapi import FastAPI
from app.routers import router as account_router
from app.auth_router import router as auth_router

app = FastAPI()

app.include_router(account_router)
app.include_router(auth_router)