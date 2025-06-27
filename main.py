from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from uuid import UUID, uuid4
from typing import Annotated


class UserBase(SQLModel):
    """Shared User props"""
    username: str = Field(unique=True, index=True)
    email: str | None = Field(default=None, unique=True)
    name: str


class User(UserBase, table=True):
    """DB model for user table"""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str

    hobby_links: list["UserHobbyLink"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    """Props to return for User"""
    id: UUID


class UserCreate(UserBase):
    """Props to receive on User creation"""
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    """Props to receive on User update"""
    pass


class HobbyBase(SQLModel):
    """Shared Hobby props"""
    name: str
    description: str | None = None


class Hobby(HobbyBase, table=True):
    """DB model for hobby table"""
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class HobbyPublic(HobbyBase):
    """Props to return for Hobby"""
    id: UUID


class HobbyCreate(HobbyBase):
    """Props to receive on Hobby creation"""
    pass


class HobbyUpdate(HobbyBase):
    """Props to receive on Hobby update"""
    pass


class UserHobbyBase(SQLModel):
    """Shared UserHobby props"""
    interested: bool = True
    rating: int | None = None


class UserHobbyLink(UserHobbyBase, table=True):
    """DB model for userhobbylink table"""
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    hobby_id: UUID = Field(foreign_key="hobby.id", primary_key=True)

    user: User = Relationship(back_populates="hobby_links")
    hobby: Hobby = Relationship()


class UserHobbyPublic(UserHobbyBase):
    """Props to return for UserHobby"""
    user_id: UUID
    hobby_id: UUID


class UserHobbyCreate(UserHobbyBase):
    """Props to receive on UserHobby creation"""
    pass


class UserHobbyUpdate(UserHobbyBase):
    """Props to receive on UserHobby update"""
    pass


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///hobby-explorer.db",
                       echo=True, connect_args=connect_args)


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


@app.post("/users", response_model=UserPublic)
def create_user(session: SessionDep, user: UserCreate):
    db_user = User.model_validate(
        user, update={"password_hash": user.password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(session: SessionDep, user_id: UUID):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
    return {"ok": True}


@app.get("/users/{user_id}/hobbies", response_model=list[HobbyPublic])
def get_user_hobbies(session: SessionDep, user_id: UUID, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    hobbies = session.exec(select(Hobby).offset(offset).limit(limit)).all()
    return hobbies


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
