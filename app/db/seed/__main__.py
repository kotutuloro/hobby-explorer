import os

from app.db.database import get_session
from .helpers import seed_hobbies_data

SEED_FILE_DIR = os.path.dirname(__file__)
HOBBIES_SEED_FILE = "hobbies.csv"


def main():
    print("seeding data")

    session = next(get_session())
    seed_path = os.path.join(SEED_FILE_DIR, HOBBIES_SEED_FILE)
    with open(seed_path, "r") as f:
        seed_hobbies_data(f, session)

    print("seeding complete")


main()
