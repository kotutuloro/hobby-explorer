from fastapi.testclient import TestClient
from sqlmodel import Session
from uuid import UUID, uuid4

from app.models import User


def test_create_user(client: TestClient, session: Session):
    user_json = {
        "username": "beeyou",
        "name": "kiko",
        "password": "ultrasecure",
    }
    resp = client.post("/users", json=user_json)
    assert resp.status_code == 200

    data = resp.json()
    assert data["username"] == user_json["username"]
    assert data["name"] == user_json["name"]
    assert data["email"] is None
    assert "password" not in data
    assert "password_hash" not in data

    db_user = session.get(User, UUID(data["id"]))
    assert db_user is not None
    assert db_user.username == user_json["username"]
    assert db_user.name == user_json["name"]
    assert db_user.email is None
    assert db_user.password_hash != user_json["password"]


def test_create_user_incomplete(client: TestClient):
    user_json = {
        "username": "beeyou",
        "password": "ultrasecure",
    }
    resp = client.post("/users", json=user_json)
    assert resp.status_code == 422


def test_create_user_existing_username(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    user_json = {
        "username": user.username,
        "name": "imposter",
        "password": "mycoolpassword",
    }
    resp = client.post("/users", json=user_json)
    assert resp.status_code == 400
    assert resp.json() == {'detail': 'This username is already taken.'}


def test_create_user_existing_email(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko",
                email="kiko@example.com", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    user_json = {
        "username": "anotheruser",
        "name": "imposter",
        "email": user.email,
        "password": "mycoolpassword",
    }
    resp = client.post("/users", json=user_json)
    assert resp.status_code == 400
    assert resp.json() == {'detail': 'A user with this email already exists.'}


def test_create_user_existing_empty_email(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    user_json = {
        "username": "mememe",
        "name": "new guy",
        "password": "mycoolpassword",
    }
    resp = client.post("/users", json=user_json)
    assert resp.status_code == 200


def test_get_user(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko",
                email="kiko@example.com", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    resp = client.get(f"/users/{user.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["username"] == user.username
    assert data["name"] == user.name
    assert data["email"] == user.email
    assert data["id"] == str(user.id)
    assert "password_hash" not in data


def test_get_user_not_found(client: TestClient):
    resp = client.get(f"/users/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}


def test_update_user(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko",
                email="kiko@example.com", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    user_json = {"email": None,
                 "username": "newusername",
                 "password": "newpassword"}
    resp = client.patch(f"/users/{user.id}", json=user_json)
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == str(user.id)
    assert data["username"] == user_json["username"]
    assert data["email"] == user_json["email"]
    assert data["name"] == user.name
    assert "password" not in data
    assert "password_hash" not in data

    db_user = session.get(User, user.id)
    assert db_user is not None
    assert db_user.username == user_json["username"]
    assert db_user.name == user.name
    assert db_user.email == user_json["email"]
    assert db_user.password_hash != user_json["password"]


def test_update_user_not_found(client: TestClient):
    resp = client.patch(f"/users/{uuid4()}", json={})
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}


def test_delete_user(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    resp = client.delete(f"/users/{user.id}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

    assert session.get(User, user.id) is None


def test_delete_user_not_found(client: TestClient):
    resp = client.delete(f"/users/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}
