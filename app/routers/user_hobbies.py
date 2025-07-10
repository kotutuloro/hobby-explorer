from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from ..dependencies import SessionDep
from ..models import *
from .users import get_user
from .hobbies import get_hobby


router = APIRouter()


@router.get("/users/{user_id}/hobbies", response_model=list[HobbyPublic])
def get_user_hobbies(session: SessionDep, user_id: UUID, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    user = get_user(session, user_id)
    hobbies = [uh.hobby for uh in user.hobby_links[offset:offset+limit]]
    return hobbies


@router.post("/users/{user_id}/hobbies", response_model=UserHobbyPublic)
def add_user_hobby(session: SessionDep, user_id: UUID, user_hobby_in: UserHobbyCreate):
    user = get_user(session, user_id)
    hobby = get_hobby(session, user_hobby_in.hobby_id)

    existing = session.get(UserHobbyLink, (user.id, hobby.id))
    if existing:
        raise HTTPException(
            status_code=400, detail="User already has this hobby")

    db_user_hobby = UserHobbyLink.model_validate(
        user_hobby_in, update={"user_id": user_id})
    session.add(db_user_hobby)
    session.commit()
    session.refresh(db_user_hobby)
    return db_user_hobby


@router.get("/users/{user_id}/hobbies/{hobby_id}", response_model=UserHobbyPublic)
def get_user_hobby(session: SessionDep, user_id: UUID, hobby_id: UUID):
    user_hobby = session.get(UserHobbyLink, (user_id, hobby_id))
    if not user_hobby:
        raise HTTPException(
            status_code=404, detail="User hobby link not found")
    return user_hobby


@router.patch("/users/{user_id}/hobbies/{hobby_id}", response_model=UserHobbyPublic)
def update_user_hobby(session: SessionDep, user_id: UUID, hobby_id: UUID, user_hobby_in: UserHobbyUpdate):
    db_user_hobby = get_user_hobby(session, user_id, hobby_id)
    update_data = user_hobby_in.model_dump(exclude_unset=True)
    db_user_hobby.sqlmodel_update(update_data)
    session.add(db_user_hobby)
    session.commit()
    session.refresh(db_user_hobby)
    return db_user_hobby


@router.delete("/users/{user_id}/hobbies/{hobby_id}")
def delete_user_hobby(session: SessionDep, user_id: UUID, hobby_id: UUID):
    user_hobby = get_user_hobby(session, user_id, hobby_id)
    session.delete(user_hobby)
    session.commit()
    return {"ok": True}


@router.get("/users/{user_id}/hobbies/suggestions")
def get_hobby_suggestions(user_id: UUID):
    return {"user_id": user_id, "suggestions": [], "message": "Hobby suggestions (placeholder)"}
