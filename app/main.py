from fastapi import FastAPI

from .models import *
from .routers import users, hobbies, user_hobbies

app = FastAPI(title="Hobby Explorer", version="0.1.0")


app.include_router(users.router)
app.include_router(hobbies.router)
app.include_router(user_hobbies.router)
