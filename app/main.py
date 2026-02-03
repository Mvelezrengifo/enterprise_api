from fastapi import FastAPI
from app.api import users, auth

app = FastAPI(title="Enterprise Operations API")

app.include_router(users.router)
app.include_router(auth.router)
