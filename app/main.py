from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.database import engine
from app.recommender import user_hobby_recommender
from app.routers import users, hobbies, user_hobbies


@asynccontextmanager
async def lifespan(app: FastAPI):
    user_hobby_recommender.load_from_sql(engine)
    yield

app = FastAPI(title="Hobby Explorer", version="0.1.0", lifespan=lifespan)


app.include_router(users.router)
app.include_router(hobbies.router)
app.include_router(user_hobbies.router)
