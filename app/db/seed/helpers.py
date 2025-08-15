
import csv
from typing import IO
from sqlmodel import Session

from app.models import Hobby


def get_hobbies_data(file: IO) -> list[Hobby]:
    reader = csv.DictReader(file)
    hobbies = [Hobby.model_validate(row) for row in reader]
    return hobbies


def seed_hobbies_data(file: IO, session: Session):
    hobbies = get_hobbies_data(file)
    session.add_all(hobbies)
    session.commit()
