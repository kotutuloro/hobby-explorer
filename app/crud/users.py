from sqlmodel import select, Session
from uuid import UUID

from app.core.security import hash_password
from app.models import User, UserCreate, UserUpdate


def create_user(session: Session, user_in: UserCreate) -> User:
    db_user = User.model_validate(
        user_in, update={"password_hash": hash_password(user_in.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_uuid(session: Session, user_id: UUID) -> User | None:
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def update_user(session: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["password_hash"] = hash_password(user_data["password"])

    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, db_user: User):
    session.delete(db_user)
    session.commit()
