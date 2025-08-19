from sqlmodel import select, Session
from uuid import UUID

from app.models import UserHobbyLink, UserHobbyCreate, UserHobbyUpdate


def create_user_hobby_link(session: Session, user_id: UUID, user_hobby_in: UserHobbyCreate) -> UserHobbyLink:
    db_user_hobby = UserHobbyLink.model_validate(
        user_hobby_in, update={"user_id": user_id})
    session.add(db_user_hobby)
    session.commit()
    session.refresh(db_user_hobby)
    return db_user_hobby


def get_user_hobby_link(session: Session, user_id: UUID, hobby_id: UUID) -> UserHobbyLink | None:
    db_link = session.get(UserHobbyLink, (user_id, hobby_id))
    return db_link


def update_user_hobby_link(session: Session, db_link: UserHobbyLink, user_hobby_in: UserHobbyUpdate) -> UserHobbyLink:
    update_data = user_hobby_in.model_dump(exclude_unset=True)
    db_link.sqlmodel_update(update_data)
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return db_link


def delete_user_hobby_link(session: Session, db_link: UserHobbyLink):
    session.delete(db_link)
    session.commit()
