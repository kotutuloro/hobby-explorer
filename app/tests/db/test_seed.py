from sqlmodel import Session, select, func
from io import StringIO
import pytest
from unittest.mock import patch

from app.models import Hobby
from app.db import seed


@pytest.fixture()
def mock_hobbies_seed_csv() -> StringIO:
    mock_hobby_data = """\
name,description,type
Photography,Using a camera,Creative
Rock Climbing,Scaling boulders,Sport
Gardening,Cultivating plants,Outdoor
"""

    return StringIO(mock_hobby_data)


def test_get_hobbies_data(mock_hobbies_seed_csv: StringIO):
    hobbies = seed.get_hobbies_data(mock_hobbies_seed_csv)
    assert len(hobbies) == 3

    h = hobbies[0]
    assert h.id is not None
    assert h.name == "Photography"
    assert h.description == "Using a camera"


def test_seed_hobbies_data(mock_hobbies_seed_csv: StringIO, session: Session):
    seed.seed_hobbies_data(mock_hobbies_seed_csv, session)

    hobby_count = session.exec(select(func.count()).select_from(Hobby)).one()
    assert hobby_count == 3

    hobby = session.exec(select(Hobby).where(Hobby.name == "Gardening")).one()
    assert hobby.id is not None
    assert hobby.description == "Cultivating plants"
