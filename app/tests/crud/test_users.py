import bcrypt
import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from uuid import uuid4

from app.models import User, UserCreate, UserUpdate, Hobby, UserHobbyLink
from app import crud


def test_create_user_success(session: Session):
    user_in = UserCreate(username="beeyou", name="kiko",
                         email="mail@example.com", password="ultrasecure")
    user = crud.create_user(session, user_in)

    assert isinstance(user, User)
    assert user.username == user_in.username
    assert user.name == user_in.name
    assert user.email == user_in.email
    assert bcrypt.checkpw(
        user_in.password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    )


def test_create_user_duplicate_username_raises(session: Session):
    first = User(username="dupe", name="one", password_hash="12345678")
    session.add(first)
    session.commit()

    with pytest.raises(IntegrityError):
        crud.create_user(session, UserCreate(username="dupe",
                                             name="two", password="abcdefghi"))


def test_create_user_duplicate_email_raises(session: Session):
    first = User(username="user1", name="one",
                 email="same@example.com", password_hash="12345678")
    session.add(first)
    session.commit()

    with pytest.raises(IntegrityError):
        crud.create_user(
            session,
            UserCreate(username="user2", name="two",
                       email="same@example.com", password="abcdefgh"),
        )


def test_get_user(session: Session):
    created = User(username="lookup", name="Lookup",
                   email="lookup@example.com", password_hash="12345678")
    session.add(created)
    session.commit()

    by_uuid = crud.get_user_by_uuid(session, created.id)
    assert by_uuid is not None
    assert by_uuid.id == created.id

    by_username = crud.get_user_by_username(session, "lookup")
    assert by_username is not None
    assert by_username.id == created.id

    by_email = crud.get_user_by_email(session, "lookup@example.com")
    assert by_email is not None
    assert by_email.id == created.id

    assert crud.get_user_by_uuid(session, uuid4()) is None
    assert crud.get_user_by_username(session, "nope") is None
    assert crud.get_user_by_email(session, "nope@example.com") is None


def test_update_user_changes_fields(session: Session):
    user = User(username="up", name="Old Name",
                email="old@example.com", password_hash="oldpassword")
    session.add(user)
    session.commit()

    updated = crud.update_user(
        session,
        user,
        UserUpdate(username="newuser", email=None, password="newpassword"),
    )

    assert updated.id == user.id
    assert updated.username == "newuser"
    assert updated.name == "Old Name"
    assert updated.email is None
    assert bcrypt.checkpw(
        "newpassword".encode('utf-8'),
        user.password_hash.encode('utf-8')
    )


def test_update_user_duplicate_username_raises(session: Session):
    user1 = User(username="userA", name="A", password_hash="passwordA")
    user2 = User(username="userB", name="B", password_hash="passwordB")
    session.add_all([user1, user2])
    session.commit()

    with pytest.raises(IntegrityError):
        crud.update_user(session, user2, UserUpdate(username=user1.username))
    session.rollback()

    refetched = session.get(User, user2.id)
    assert refetched is not None
    assert refetched.username == "userB"


def test_update_user_duplicate_email_raises(session: Session):
    user1 = User(username="userA", name="A",
                 email="A@A.com", password_hash="passwordA")
    user2 = User(username="userB", name="B",
                 email="B@B.com", password_hash="passwordB")
    session.add_all([user1, user2])
    session.commit()

    with pytest.raises(IntegrityError):
        crud.update_user(session, user2, UserUpdate(email=user1.email))
    session.rollback()

    refetched = session.get(User, user2.id)
    assert refetched is not None
    assert refetched.email == "B@B.com"


def test_delete_user_removes_record(session: Session):
    user = User(username="todelete", name="Del", password_hash="password")
    hobby = Hobby(name="Chess")
    link = UserHobbyLink(user_id=user.id, hobby_id=hobby.id)
    session.add_all([hobby, user, link])
    session.commit()

    crud.delete_user(session, user)
    assert session.get(User, user.id) is None
    assert session.get(UserHobbyLink, (user.id, hobby.id)) is None
