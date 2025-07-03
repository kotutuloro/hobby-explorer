from fastapi import FastAPI

from .models import *
from .database import create_db_and_tables
from .routers import users, hobbies, user_hobbies

app = FastAPI(title="Hobby Explorer", version="0.1.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(users.router)
app.include_router(hobbies.router)
app.include_router(user_hobbies.router)
