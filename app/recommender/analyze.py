import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.engine import Connectable

from app.models import Hobby, UserHobbyLink


def analyze(db_conn: Connectable):
    user_hobby_df = pd.read_sql_table(
        UserHobbyLink.__tablename__, db_conn)
    hobby_df = pd.read_sql_table(Hobby.__tablename__, db_conn)

    if len(user_hobby_df) < 50:
        init_data = dummy_user_hobby_data(hobby_df.id)
        user_hobby_df = pd.concat(
            [init_data, user_hobby_df], ignore_index=True)

    analysis = analyze_ratings(user_hobby_df)
    user_sim_df = analysis["user_similarities"]
    hobby_sim_df = analysis["hobby_similarities"]

    # todo: save to feather file?


def dummy_user_hobby_data(hobby_id_series: pd.Series) -> pd.DataFrame:
    # todo: maybe do content-based rec first instead of random
    rng = np.random.default_rng(seed=12348427)
    content = []
    for dummy_user_id in range(5):
        size = rng.integers(1, 11)
        hobby_ids = hobby_id_series.sample(
            size, random_state=rng, ignore_index=True)  # type: ignore
        interested = rng.random(size) > 0.5
        ratings = rng.integers(0, 6, size=size)

        dummy_data = pd.DataFrame(
            {
                "user_id": f"dummy-user-{dummy_user_id}",
                "hobby_id": hobby_ids,
                "interested": interested,
                "rating": ratings,
            }
        )
        content.append(dummy_data)

    return pd.concat(content, ignore_index=True)


def analyze_ratings(user_hobby_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # todo: involve the interested column somehow?
    user_hobby_matrix = user_hobby_df.pivot_table(
        index="user_id", columns="hobby_id", values="rating").fillna(0)

    user_similarity_df = pd.DataFrame(
        cosine_similarity(user_hobby_matrix),
        index=user_hobby_matrix.index,
        columns=user_hobby_matrix.index
    )

    hobby_similarity_df = pd.DataFrame(
        cosine_similarity(user_hobby_matrix.T),
        index=user_hobby_matrix.columns,
        columns=user_hobby_matrix.columns
    )

    return {
        "matrix": user_hobby_matrix,
        "user_similarities": user_similarity_df,
        "hobby_similarities": hobby_similarity_df,
    }


def get_user_recommendations(user_id: str, user_similarity_df: pd.DataFrame, user_hobby_matrix: pd.DataFrame, num_recs=2, num_users=10) -> pd.Series:
    # todo: get user_sim_df[user_id] adn user_hobby_matrix from file

    # todo: load current user ratings from db instead?
    user_ratings = user_hobby_matrix.loc[user_id]
    recs = pd.Series(dtype=float)

    similars = user_similarity_df[user_id].sort_values(ascending=False).index
    similars = similars[similars != user_id][:num_users]

    for similar_user in similars:
        similar_ratings = user_hobby_matrix.loc[similar_user]
        recs = recs.add(similar_ratings[user_ratings == 0], fill_value=0.0)

    return recs[recs > 0].nlargest(num_recs)
