from fastapi.testclient import TestClient
from sqlmodel import Session
from uuid import UUID, uuid4

from app.models import Hobby


def test_create_hobby(client: TestClient, session: Session):
    hobby_json = {
        "name": "Origami",
        "description": "Paper folding art"
    }
    resp = client.post("/hobbies", json=hobby_json)
    assert resp.status_code == 200

    data = resp.json()
    assert data["name"] == hobby_json["name"]
    assert data["description"] == hobby_json["description"]
    assert "id" in data

    db_hobby = session.get(Hobby, UUID(data["id"]))
    assert db_hobby is not None
    assert db_hobby.name == hobby_json["name"]
    assert db_hobby.description == hobby_json["description"]


def test_create_hobby_incomplete(client: TestClient):
    hobby_json = {
        "description": "Missing name"
    }
    resp = client.post("/hobbies", json=hobby_json)
    assert resp.status_code == 422


def test_create_hobby_existing_name(client: TestClient, session: Session):
    hobby = Hobby(name="Origami", description="Paper folding art")
    session.add(hobby)
    session.commit()

    hobby_json = {
        "name": hobby.name,
        "description": "Some other description"
    }
    resp = client.post("/hobbies", json=hobby_json)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Hobby already exists"}


def test_get_hobby(client: TestClient, session: Session):
    hobby = Hobby(name="Knitting", description="Crafts")
    session.add(hobby)
    session.commit()

    resp = client.get(f"/hobbies/{hobby.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == str(hobby.id)
    assert data["name"] == hobby.name
    assert data["description"] == hobby.description


def test_get_hobby_not_found(client: TestClient):
    resp = client.get(f"/hobbies/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Hobby not found"}


def test_delete_hobby(client: TestClient, session: Session):
    hobby = Hobby(name="Chess", description="Board game")
    session.add(hobby)
    session.commit()

    resp = client.delete(f"/hobbies/{hobby.id}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

    assert session.get(Hobby, hobby.id) is None


def test_delete_hobby_not_found(client: TestClient):
    resp = client.delete(f"/hobbies/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Hobby not found"}
