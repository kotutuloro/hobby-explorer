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
