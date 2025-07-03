from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..dependencies import SessionDep
from ..models import *


router = APIRouter()


@router.post("/users", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):
    existing_user = session.exec(select(User).where(
        User.username == user_in.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="This username is already taken.")

    if user_in.email:
        existing_user = session.exec(select(User).where(
            User.email == user_in.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists.")

    # TODO: password hashing
    db_user = User.model_validate(
        user_in, update={"password_hash": user_in.password})
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


@router.patch("/users/{user_id}", response_model=UserPublic)
def update_user(session: SessionDep, user_id: UUID, user_in: UserUpdate):
    db_user = get_user(session, user_id)

    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data:
        # TODO: password hashing
        password_hash = user_data["password"]
        user_data["password_hash"] = password_hash

    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(session: SessionDep, user_id: UUID):
    user = get_user(session, user_id)

    session.delete(user)
    session.commit()
    return {"ok": True}
