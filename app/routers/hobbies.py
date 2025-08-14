from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from app.dependencies import SessionDep
from app.models import *


router = APIRouter()


@router.post("/hobbies", response_model=HobbyPublic)
def create_hobby(session: SessionDep, hobby_in: HobbyCreate):
    existing_hobby = session.exec(select(Hobby).where(
        Hobby.name == hobby_in.name)).first()
    if existing_hobby:
        raise HTTPException(status_code=400, detail="Hobby already exists")

    db_hobby = Hobby.model_validate(hobby_in)
    session.add(db_hobby)
    session.commit()
    session.refresh(db_hobby)
    return db_hobby


@router.get("/hobbies/{hobby_id}", response_model=HobbyPublic)
def get_hobby(session: SessionDep, hobby_id: UUID):
    hobby = session.get(Hobby, hobby_id)
    if not hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")
    return hobby


@router.delete("/hobbies/{hobby_id}")
def delete_hobby(session: SessionDep, hobby_id: UUID):
    hobby = get_hobby(session, hobby_id)
    session.delete(hobby)
    session.commit()
    return {"ok": True}
