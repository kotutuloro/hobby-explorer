import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.engine import Engine
from typing import Generator

from app.database import get_session
from app.main import app
from app.config import settings


@pytest.fixture
def engine() -> Engine:
    engine = create_engine(f"{settings.TEST_DATABASE_URL}", echo=True)
    return engine


@pytest.fixture(autouse=True)
def cleanup(engine: Engine):
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()
