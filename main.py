from fastapi import FastAPI
from pydantic import BaseModel


class UserHobby(BaseModel):
    interested: bool
    tried: bool
    enjoyed: bool


class UserHobbyWithID(UserHobby):
    hobby_id: int


class User(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    hobbies: list[UserHobbyWithID] | None = None


class Hobby(BaseModel):
    name: str
    description: str | None = None


app = FastAPI()


@app.post("/users")
def create_user(user: User):
    return {"user": user, "message": "User created (placeholder)"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "message": "Get user (placeholder)"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {"user_id": user_id, "user": user, "message": "Update user (placeholder)"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"user_id": user_id, "message": "Delete user (placeholder)"}


@app.get("/users/{user_id}/hobbies")
def get_user_hobbies(user_id: int):
    return {"user_id": user_id, "hobbies": [], "message": "Get user hobbies (placeholder)"}


@app.post("/users/{user_id}/hobbies")
def add_user_hobby(user_id: int, user_hobby: UserHobbyWithID):
    return {"user_id": user_id, "user_hobby": user_hobby, "message": "Add hobby to user (placeholder)"}


@app.get("/users/{user_id}/hobbies/{hobby_id}")
def get_user_hobby(user_id: int, hobby_id: int):
    return {"user_id": user_id, "hobby_id": hobby_id, "message": "Get user hobby (placeholder)"}


@app.put("/users/{user_id}/hobbies/{hobby_id}")
def update_user_hobby(user_id: int, hobby_id: int, user_hobby: UserHobby):
    return {"user_id": user_id, "hobby_id": hobby_id, "user_hobby": user_hobby, "message": "Update user hobby (placeholder)"}


@app.delete("/users/{user_id}/hobbies/{hobby_id}")
def delete_user_hobby(user_id: int, hobby_id: int):
    return {"user_id": user_id, "hobby_id": hobby_id, "message": "Delete user hobby (placeholder)"}


@app.get("/users/{user_id}/hobbies/suggestions")
def get_hobby_suggestions(user_id: int):
    return {"user_id": user_id, "suggestions": [], "message": "Hobby suggestions (placeholder)"}


@app.post("/hobbies")
def create_hobby(hobby: Hobby):
    return {"hobby": hobby, "message": "Hobby created (placeholder)"}


@app.get("/hobbies/{hobby_id}")
def get_hobby(hobby_id: int):
    return {"hobby_id": hobby_id, "message": "Get hobby (placeholder)"}


@app.delete("/hobbies/{hobby_id}")
def delete_hobby(hobby_id: int):
    return {"hobby_id": hobby_id, "message": "Delete hobby (placeholder)"}
