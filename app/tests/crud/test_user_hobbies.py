import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from uuid import uuid4

from app.models import User, Hobby, UserHobbyLink, UserHobbyCreate, UserHobbyUpdate
from app import crud


def _make_user_and_hobby(session: Session) -> tuple[User, Hobby]:
    user = User(username="linkuser", name="Link User",
                password_hash="pw12345678")
    hobby = Hobby(name="Gardening")
    session.add_all([user, hobby])
    session.commit()
    session.refresh(user)
    session.refresh(hobby)
    return user, hobby


def test_create_user_hobby_link_success(session: Session):
    user, hobby = _make_user_and_hobby(session)

    link_in = UserHobbyCreate(hobby_id=hobby.id)
    link = crud.create_user_hobby_link(session, user.id, link_in)

    assert isinstance(link, UserHobbyLink)
    assert link.user_id == user.id
    assert link.hobby_id == hobby.id
    assert link.interested is True
    assert link.rating is None


def test_create_user_hobby_link_duplicate_raises(session: Session):
    user, hobby = _make_user_and_hobby(session)

    first = UserHobbyLink(user_id=user.id, hobby_id=hobby.id)
    session.add(first)
    session.commit()

    with pytest.raises(IntegrityError):
        crud.create_user_hobby_link(
            session, user.id, UserHobbyCreate(hobby_id=hobby.id))


def test_get_user_hobby_link(session: Session):
    user, hobby = _make_user_and_hobby(session)
    created = UserHobbyLink(user_id=user.id, hobby_id=hobby.id)
    session.add(created)
    session.commit()

    fetched = crud.get_user_hobby_link(session, user.id, hobby.id)
    assert fetched is not None
    assert fetched.user_id == created.user_id
    assert fetched.hobby_id == created.hobby_id

    assert crud.get_user_hobby_link(session, uuid4(), hobby.id) is None
    assert crud.get_user_hobby_link(session, user.id, uuid4()) is None


def test_update_user_hobby_link_changes_fields(session: Session):
    user, hobby = _make_user_and_hobby(session)
    created = UserHobbyLink(user_id=user.id, hobby_id=hobby.id)
    session.add(created)
    session.commit()

    updated = crud.update_user_hobby_link(
        session,
        created,
        UserHobbyUpdate(interested=False, rating=5),
    )

    assert updated.user_id == created.user_id
    assert updated.hobby_id == created.hobby_id
    assert updated.interested is False
    assert updated.rating == 5


def test_delete_user_hobby_link_removes_record(session: Session):
    user, hobby = _make_user_and_hobby(session)
    link = UserHobbyLink(user_id=user.id, hobby_id=hobby.id)
    session.add(link)
    session.commit()

    crud.delete_user_hobby_link(session, link)
    assert session.get(UserHobbyLink, (user.id, hobby.id)) is None
    assert session.get(User, user.id) is not None
    assert session.get(Hobby, hobby.id) is not None
