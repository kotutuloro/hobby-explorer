
import csv
from typing import IO, Any
from pydantic import ValidationError
from sqlmodel import Session
from sqlalchemy.dialects.postgresql import insert

from app.models import Hobby


def get_hobbies_data(file: IO) -> list[dict[str, Any]]:
    reader = csv.DictReader(file)
    hobbies = []
    for row in reader:
        try:
            hobby = Hobby.model_validate(row)
        except ValidationError as e:
            print("Invalid hobby data:", row, e)
        else:
            hobbies.append(hobby.model_dump())
    return hobbies


def seed_hobbies_data(file: IO, session: Session):
    hobbies = get_hobbies_data(file)
    statement = insert(Hobby).values(hobbies).on_conflict_do_nothing()
    session.execute(statement)
    session.commit()
