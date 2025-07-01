from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from ..dependencies import SessionDep
from ..models import *


router = APIRouter()


@router.post("/users", response_model=UserPublic)
def create_user(session: SessionDep, user: UserCreate):
    db_user = User.model_validate(
        user, update={"password_hash": user.password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=UserPublic)
def get_user(session: SessionDep, user_id: UUID):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}")
def update_user(user_id: UUID, user: User):
    return {"user_id": user_id, "user": user, "message": "Update user (placeholder)"}


@router.delete("/users/{user_id}")
def delete_user(session: SessionDep, user_id: UUID):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@router.get("/users/{user_id}/hobbies", response_model=list[HobbyPublic])
def get_user_hobbies(session: SessionDep, user_id: UUID, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    hobbies = session.exec(select(Hobby).offset(offset).limit(limit)).all()
    return hobbies


@router.post("/users/{user_id}/hobbies")
def add_user_hobby(user_id: UUID, user_hobby: UserHobbyLink):
    return {"user_id": user_id, "user_hobby": user_hobby, "message": "Add hobby to user (placeholder)"}


@router.get("/users/{user_id}/hobbies/{hobby_id}")
def get_user_hobby(user_id: UUID, hobby_id: UUID):
    return {"user_id": user_id, "hobby_id": hobby_id, "message": "Get user hobby (placeholder)"}


@router.put("/users/{user_id}/hobbies/{hobby_id}")
def update_user_hobby(user_id: UUID, hobby_id: UUID, user_hobby: UserHobbyBase):
    return {"user_id": user_id, "hobby_id": hobby_id, "user_hobby": user_hobby, "message": "Update user hobby (placeholder)"}


@router.delete("/users/{user_id}/hobbies/{hobby_id}")
def delete_user_hobby(user_id: UUID, hobby_id: UUID):
    return {"user_id": user_id, "hobby_id": hobby_id, "message": "Delete user hobby (placeholder)"}


@router.get("/users/{user_id}/hobbies/suggestions")
def get_hobby_suggestions(user_id: UUID):
    return {"user_id": user_id, "suggestions": [], "message": "Hobby suggestions (placeholder)"}
