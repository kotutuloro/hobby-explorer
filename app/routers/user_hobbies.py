from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from ..dependencies import SessionDep
from ..models import *


router = APIRouter()


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
