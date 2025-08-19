from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.dependencies import SessionDep
from app.models import UserPublic, UserCreate, UserUpdate
from app import crud


router = APIRouter()


@router.post("/users", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):
    existing_user = crud.get_user_by_username(session, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="This username is already taken.")

    if user_in.email:
        existing_user = crud.get_user_by_email(session, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists.")

    user = crud.create_user(session, user_in)
    return user


@router.get("/users/{user_id}", response_model=UserPublic)
def get_user(session: SessionDep, user_id: UUID):
    user = crud.get_user_by_uuid(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserPublic)
def update_user(session: SessionDep, user_id: UUID, user_in: UserUpdate):
    db_user = crud.get_user_by_uuid(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = crud.update_user(session, db_user, user_in)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(session: SessionDep, user_id: UUID):
    db_user = crud.get_user_by_uuid(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(session, db_user)
    return {"ok": True}
