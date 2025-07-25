import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.engine import Engine
from typing import Generator
import alembic
from alembic.config import Config as AlembicConfig

from app.database import get_session
from app.main import app
from app.config import settings


@pytest.fixture
def engine() -> Engine:
    engine = create_engine(f"{settings.TEST_DATABASE_URL}", echo=True)
    return engine


@pytest.fixture(autouse=True)
def apply_migrations(engine: Engine):
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.attributes["connection"] = engine
    alembic.command.upgrade(alembic_cfg, "head")
    yield
    alembic.command.downgrade(alembic_cfg, "base")


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()
