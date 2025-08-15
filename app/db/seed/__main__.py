
from app.db.database import get_session
from .helpers import seed_hobbies_data


HOBBIES_SEED_FILE = "hobbies.csv"


def main():
    print("seeding data")

    session = get_session()
    with open(HOBBIES_SEED_FILE, "r") as f:
        seed_hobbies_data(f, session)

    print("seeding complete")


main()
