import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.engine import Engine
from typing import Generator

from app.database import get_session
from app.main import app


@pytest.fixture(scope="session")
def engine() -> Engine:
    connect_args = {"check_same_thread": False}
    engine = create_engine("sqlite:///hobby-explorer-tests.db",
                           connect_args=connect_args)
    return engine


@pytest.fixture(autouse=True)
def cleanup(engine: Engine) -> Generator[None, None, None]:
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
