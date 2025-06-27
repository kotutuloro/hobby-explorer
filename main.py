from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from uuid import UUID, uuid4
from typing import Annotated


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str | None = Field(default=None, unique=True)
    password_hash: str
    name: str

    hobby_links: list["UserHobbyLink"] = Relationship(back_populates="user")


class Hobby(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str | None = None


class UserHobbyBase(SQLModel):
    interested: bool = True
    rating: int | None = None


class UserHobbyLink(UserHobbyBase, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    hobby_id: UUID = Field(foreign_key="hobby.id", primary_key=True)

    user: User = Relationship(back_populates="hobby_links")
    hobby: Hobby = Relationship()


engine = create_engine("sqlite:///hobby-explorer.db", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users")
def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"user": user, "message": "User created (placeholder)"}


@app.get("/users/{user_id}")
def get_user(user_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user, "message": "Get user (placeholder)"}


@app.put("/users/{user_id}")
def update_user(user_id: UUID, user: User):
    return {"user_id": user_id, "user": user, "message": "Update user (placeholder)"}


@app.delete("/users/{user_id}")
def delete_user(session: SessionDep, user_id: UUID):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"user_id": user_id, "message": "Deleted user (placeholder)"}


@app.get("/users/{user_id}/hobbies")
def get_user_hobbies(session: SessionDep, user_id: UUID, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    hobbies = session.exec(select(Hobby).offset(offset).limit(limit)).all()
    return {"user_id": user_id, "hobbies": hobbies, "message": "Get user hobbies (placeholder)"}


@app.post("/users/{user_id}/hobbies")
def add_user_hobby(user_id: UUID, user_hobby: UserHobbyLink):
    return {"user_id": user_id, "user_hobby": user_hobby, "message": "Add hobby to user (placeholder)"}


@app.get("/users/{user_id}/hobbies/{hobby_id}")
def get_user_hobby(user_id: UUID, hobby_id: UUID):
    return {"user_id": user_id, "hobby_id": hobby_id, "message": "Get user hobby (placeholder)"}


@app.put("/users/{user_id}/hobbies/{hobby_id}")
def update_user_hobby(user_id: UUID, hobby_id: UUID, user_hobby: UserHobbyBase):
    return {"user_id": user_id, "hobby_id": hobby_id, "user_hobby": user_hobby, "message": "Update user hobby (placeholder)"}


@app.delete("/users/{user_id}/hobbies/{hobby_id}")
def delete_user_hobby(user_id: UUID, hobby_id: UUID):
    return {"user_id": user_id, "hobby_id": hobby_id, "message": "Delete user hobby (placeholder)"}


@app.get("/users/{user_id}/hobbies/suggestions")
def get_hobby_suggestions(user_id: UUID):
    return {"user_id": user_id, "suggestions": [], "message": "Hobby suggestions (placeholder)"}


@app.post("/hobbies")
def create_hobby(hobby: Hobby):
    return {"hobby": hobby, "message": "Hobby created (placeholder)"}


@app.get("/hobbies/{hobby_id}")
def get_hobby(hobby_id: UUID):
    return {"hobby_id": hobby_id, "message": "Get hobby (placeholder)"}


@app.delete("/hobbies/{hobby_id}")
def delete_hobby(hobby_id: UUID):
    return {"hobby_id": hobby_id, "message": "Delete hobby (placeholder)"}
