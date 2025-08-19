import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from uuid import uuid4

from app.models import Hobby, HobbyCreate, User, UserHobbyLink
from app import crud


def test_create_hobby_success(session: Session):
    hobby_in = HobbyCreate(name="Chess", description="Board game")
    hobby = crud.create_hobby(session, hobby_in)

    assert isinstance(hobby, Hobby)
    assert hobby.name == hobby_in.name
    assert hobby.description == hobby_in.description


def test_create_hobby_duplicate_name_raises(session: Session):
    first = Hobby(name="Duplicate", description="First")
    session.add(first)
    session.commit()

    with pytest.raises(IntegrityError):
        crud.create_hobby(session, HobbyCreate(
            name="Duplicate", description="Second"))


def test_get_hobby(session: Session):
    created = Hobby(name="Hiking", description="Trails")
    session.add(created)
    session.commit()

    by_uuid = crud.get_hobby_by_uuid(session, created.id)
    assert by_uuid is not None
    assert by_uuid.id == created.id

    by_name = crud.get_hobby_by_name(session, "Hiking")
    assert by_name is not None
    assert by_name.id == created.id

    assert crud.get_hobby_by_uuid(session, uuid4()) is None
    assert crud.get_hobby_by_name(session, "Nope") is None


def test_delete_hobby_removes_record(session: Session):
    user = User(username="user_delete_hobby",
                name="User", password_hash="password")
    hobby = Hobby(name="DeleteMe")
    link = UserHobbyLink(user_id=user.id, hobby_id=hobby.id)
    session.add_all([user, hobby, link])
    session.commit()

    crud.delete_hobby(session, hobby)
    assert session.get(Hobby, hobby.id) is None
    assert session.get(UserHobbyLink, (user.id, hobby.id)) is None
