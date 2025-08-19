from sqlmodel import select, Session
from uuid import UUID

from app.models import Hobby, HobbyCreate


def create_hobby(session: Session, hobby_in: HobbyCreate) -> Hobby:
    db_hobby = Hobby.model_validate(hobby_in)
    session.add(db_hobby)
    session.commit()
    session.refresh(db_hobby)
    return db_hobby


def get_hobby_by_uuid(session: Session, hobby_id: UUID) -> Hobby | None:
    return session.get(Hobby, hobby_id)


def get_hobby_by_name(session: Session, hobby_name: str) -> Hobby | None:
    statement = select(Hobby).where(Hobby.name == hobby_name)
    hobby = session.exec(statement).first()
    return hobby


def delete_hobby(session: Session, db_hobby: Hobby):
    session.delete(db_hobby)
    session.commit()
