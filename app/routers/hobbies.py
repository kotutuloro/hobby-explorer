from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.dependencies import SessionDep
from app.models import HobbyPublic, HobbyCreate
from app import crud


router = APIRouter()


@router.post("/hobbies", response_model=HobbyPublic)
def create_hobby(session: SessionDep, hobby_in: HobbyCreate):
    existing_hobby = crud.get_hobby_by_name(session, hobby_in.name)
    if existing_hobby:
        raise HTTPException(status_code=400, detail="Hobby already exists")

    db_hobby = crud.create_hobby(session, hobby_in)
    return db_hobby


@router.get("/hobbies/{hobby_id}", response_model=HobbyPublic)
def get_hobby(session: SessionDep, hobby_id: UUID):
    db_hobby = crud.get_hobby_by_uuid(session, hobby_id)
    if not db_hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")
    return db_hobby


@router.delete("/hobbies/{hobby_id}")
def delete_hobby(session: SessionDep, hobby_id: UUID):
    db_hobby = crud.get_hobby_by_uuid(session, hobby_id)
    if not db_hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")

    crud.delete_hobby(session, db_hobby)
    return {"ok": True}
