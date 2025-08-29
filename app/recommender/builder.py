from app.db.database import engine
from . import user_hobby_recommender


if __name__ == "__main__":
    user_hobby_recommender.load_from_sql(engine)
    user_hobby_recommender.dump_to_feather()
