from fastapi.testclient import TestClient
from sqlmodel import Session
from uuid import uuid4

from app.models import User, Hobby, UserHobbyLink


def test_get_user_hobbies(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby1 = Hobby(name="Chess", description="Board game")
    hobby2 = Hobby(name="Painting", description="Art")
    unused_hobby = Hobby(name="Knitting", description="Crafts")
    hobby_link1 = UserHobbyLink(
        user=user, hobby=hobby1, interested=True, rating=5)
    hobby_link2 = UserHobbyLink(user=user, hobby=hobby2, interested=False)
    session.add_all([user, hobby1, hobby2, hobby_link1,
                    hobby_link2, unused_hobby])
    session.commit()

    resp = client.get(f"/users/{user.id}/hobbies")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert any(h["name"] == "Chess" for h in data)
    assert any(h["name"] == "Painting" for h in data)
    assert not any(h["name"] == "Knitting" for h in data)


def test_get_user_hobbies_not_found(client: TestClient):
    resp = client.get(f"/users/{uuid4()}/hobbies")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}


def test_add_user_hobby(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    session.add_all([user, hobby])
    session.commit()

    user_hobby_json = {
        "hobby_id": str(hobby.id),
        "interested": True,
        "rating": 5
    }
    resp = client.post(f"/users/{user.id}/hobbies", json=user_hobby_json)
    assert resp.status_code == 200

    data = resp.json()
    assert data["user_id"] == str(user.id)
    assert data["hobby_id"] == str(hobby.id)
    assert data["interested"] == user_hobby_json["interested"]
    assert data["rating"] == user_hobby_json["rating"]

    db_user_hobby = session.get(UserHobbyLink, (user.id, hobby.id))
    assert db_user_hobby is not None
    assert db_user_hobby.interested is True
    assert db_user_hobby.rating == 5


def test_add_user_hobby_duplicate(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    user_hobby = UserHobbyLink(
        user=user, hobby=hobby, interested=True, rating=5)
    session.add_all([user, hobby, user_hobby])
    session.commit()

    user_hobby_json = {
        "hobby_id": str(hobby.id),
        "interested": False,
        "rating": 2
    }
    resp = client.post(f"/users/{user.id}/hobbies", json=user_hobby_json)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "User already has this hobby"}


def test_add_user_hobby_user_not_found(client: TestClient, session: Session):
    hobby = Hobby(name="Chess", description="Board game")
    session.add(hobby)
    session.commit()

    user_hobby_json = {
        "hobby_id": str(hobby.id),
        "interested": True,
        "rating": 5
    }
    resp = client.post(
        f"/users/{uuid4()}/hobbies", json=user_hobby_json)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}


def test_add_user_hobby_hobby_not_found(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    session.add(user)
    session.commit()

    user_hobby_json = {
        "hobby_id": str(uuid4()),
        "interested": True,
        "rating": 5
    }
    resp = client.post(f"/users/{user.id}/hobbies", json=user_hobby_json)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Hobby not found"}


def test_get_user_hobby(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    user_hobby = UserHobbyLink(user_id=user.id, hobby_id=hobby.id,
                               interested=True, rating=5)
    session.add_all([user, hobby, user_hobby])
    session.commit()

    resp = client.get(f"/users/{user.id}/hobbies/{hobby.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["user_id"] == str(user.id)
    assert data["hobby_id"] == str(hobby.id)
    assert data["interested"] == user_hobby.interested
    assert data["rating"] == user_hobby.rating


def test_get_user_hobby_not_found(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    session.add_all([user, hobby])
    session.commit()

    resp = client.get(f"/users/{user.id}/hobbies/{hobby.id}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User hobby link not found"}


def test_update_user_hobby(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    user_hobby = UserHobbyLink(
        user=user, hobby=hobby, interested=True, rating=5)
    session.add_all([user, hobby, user_hobby])
    session.commit()

    update_json = {"interested": False, "rating": 2}
    resp = client.put(f"/users/{user.id}/hobbies/{hobby.id}", json=update_json)
    assert resp.status_code == 200

    data = resp.json()
    assert data["user_id"] == str(user.id)
    assert data["hobby_id"] == str(hobby.id)
    assert data["interested"] == user_hobby.interested
    assert data["rating"] == user_hobby.rating

    user_hobby_db = session.get(UserHobbyLink, (user.id, hobby.id))
    assert user_hobby_db is not None
    assert user_hobby_db.interested is False
    assert user_hobby_db.rating == 2


def test_update_user_hobby_not_found(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    session.add_all([user, hobby])
    session.commit()

    update_json = {"interested": False, "rating": 2}
    resp = client.put(f"/users/{user.id}/hobbies/{hobby.id}", json=update_json)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User hobby link not found"}


def test_delete_user_hobby(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    user_hobby = UserHobbyLink(
        user=user, hobby=hobby, interested=True, rating=5)
    session.add_all([user, hobby, user_hobby])
    session.commit()

    resp = client.delete(f"/users/{user.id}/hobbies/{hobby.id}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

    user_hobby_db = session.get(UserHobbyLink, (user.id, hobby.id))
    assert user_hobby_db is None


def test_delete_user_hobby_not_found(client: TestClient, session: Session):
    user = User(username="beeyou", name="kiko", password_hash="ultrasecure")
    hobby = Hobby(name="Chess", description="Board game")
    session.add_all([user, hobby])
    session.commit()

    resp = client.delete(f"/users/{user.id}/hobbies/{hobby.id}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User hobby link not found"}
