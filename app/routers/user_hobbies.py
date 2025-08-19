from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from uuid import UUID

from app.dependencies import SessionDep
from app.models import UserHobbyPublic, UserHobbyCreate, UserHobbyUpdate, HobbyPublic
from app import crud


router = APIRouter()


@router.get("/users/{user_id}/hobbies", response_model=list[HobbyPublic])
def get_user_hobbies(session: SessionDep, user_id: UUID, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    user = crud.get_user_by_uuid(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hobbies = [uh.hobby for uh in user.hobby_links[offset:offset+limit]]
    return hobbies


@router.post("/users/{user_id}/hobbies", response_model=UserHobbyPublic)
def add_user_hobby(session: SessionDep, user_id: UUID, user_hobby_in: UserHobbyCreate):
    user = crud.get_user_by_uuid(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hobby = crud.get_hobby_by_uuid(session, user_hobby_in.hobby_id)
    if not hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")

    existing = crud.get_user_hobby_link(
        session, user_id=user.id, hobby_id=hobby.id)
    if existing:
        raise HTTPException(
            status_code=400, detail="User already has this hobby")

    db_user_hobby = crud.create_user_hobby_link(
        session, user_id, user_hobby_in)
    return db_user_hobby


@router.get("/users/{user_id}/hobbies/{hobby_id}", response_model=UserHobbyPublic)
def get_user_hobby(session: SessionDep, user_id: UUID, hobby_id: UUID):
    user_hobby = crud.get_user_hobby_link(
        session, user_id=user_id, hobby_id=hobby_id)
    if not user_hobby:
        raise HTTPException(
            status_code=404, detail="User hobby link not found")
    return user_hobby


@router.patch("/users/{user_id}/hobbies/{hobby_id}", response_model=UserHobbyPublic)
def update_user_hobby(session: SessionDep, user_id: UUID, hobby_id: UUID, user_hobby_in: UserHobbyUpdate):
    db_user_hobby = crud.get_user_hobby_link(
        session, user_id=user_id, hobby_id=hobby_id)
    if not db_user_hobby:
        raise HTTPException(
            status_code=404, detail="User hobby link not found")

    db_user_hobby = crud.update_user_hobby_link(
        session, db_user_hobby, user_hobby_in)
    return db_user_hobby


@router.delete("/users/{user_id}/hobbies/{hobby_id}")
def delete_user_hobby(session: SessionDep, user_id: UUID, hobby_id: UUID):
    db_user_hobby = crud.get_user_hobby_link(
        session, user_id=user_id, hobby_id=hobby_id)
    if not db_user_hobby:
        raise HTTPException(
            status_code=404, detail="User hobby link not found")

    crud.delete_user_hobby_link(session, db_user_hobby)
    return {"ok": True}


@router.get("/users/{user_id}/hobbies/suggestions")
def get_hobby_suggestions(user_id: UUID):
    return {"user_id": user_id, "suggestions": [], "message": "Hobby suggestions (placeholder)"}
