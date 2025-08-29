from uuid import UUID, uuid4
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
from sqlalchemy.engine import Connectable

from app.models import Hobby, UserHobbyLink


class _UserHobbyRecommender():
    def __init__(self,):
        self._user_hobby_matrix = None
        self._user_similarity_df = None
        self._hobby_similarity_df = None

    def load_from_sql(self, db_conn: Connectable, include_dummy: bool = True):
        user_hobby_df = pd.read_sql_table(
            UserHobbyLink.__tablename__, db_conn)

        if include_dummy and len(user_hobby_df) < 50:
            hobby_df = pd.read_sql_table(Hobby.__tablename__, db_conn)
            init_data = self._dummy_user_hobby_data(hobby_df.id)
            user_hobby_df = pd.concat(
                [init_data, user_hobby_df], ignore_index=True)

        self._analyze_ratings(user_hobby_df)

    def load_from_feather(self):
        pass

    def dump_to_feather(self):
        pass

    def get_hobby_recs_for_user(
        self,
        user_id: UUID,
        num_recs: int = 2,
        num_similar_users: int = 10
    ) -> list[UUID]:

        if self._user_hobby_matrix is None or self._user_similarity_df is None:
            raise AttributeError(
                f"Missing required dataframe attributes. Refresh data with `load_from_feather` or `load_from_sql`.")

        recs = pd.Series(dtype=float)
        # todo: try/catch for user_id name errors
        # todo: load current user ratings from db instead?
        user_ratings = self._user_hobby_matrix.loc[user_id]
        similars = self._user_similarity_df[user_id].sort_values(
            ascending=False).index[1:num_similar_users+1]

        for similar_user in similars:
            similar_ratings = self._user_hobby_matrix.loc[similar_user]
            recs = recs.add(similar_ratings[user_ratings == 0], fill_value=0.0)

        top_hobbies = recs[recs > 0].nlargest(num_recs)
        return top_hobbies.index.to_list()

    def get_similar_hobbies(self, hobby_id: UUID, num_recs: int = 2) -> list[UUID]:
        similars = self._hobby_similarity_df[hobby_id]
        top_hobbies = similars[similars > 0].nlargest(num_recs+1)[1:]
        return top_hobbies.index.to_list()

    def _analyze_ratings(self, user_hobby_df: pd.DataFrame):
        # todo: involve the interested column somehow?
        self._user_hobby_matrix = user_hobby_df.pivot_table(
            index="user_id", columns="hobby_id", values="rating").fillna(0)

        self._user_similarity_df = pd.DataFrame(
            cosine_similarity(self._user_hobby_matrix),
            index=self._user_hobby_matrix.index,
            columns=self._user_hobby_matrix.index
        )

        self._hobby_similarity_df = pd.DataFrame(
            cosine_similarity(self._user_hobby_matrix.T),
            index=self._user_hobby_matrix.columns,
            columns=self._user_hobby_matrix.columns
        )

    @staticmethod
    def _dummy_user_hobby_data(hobby_id_series: pd.Series) -> pd.DataFrame:
        # todo: maybe do content-based rec first instead of random
        rng = np.random.default_rng(seed=12348427)
        content = []
        for _ in range(100):
            size = int(rng.integers(1, 20))
            hobby_ids = hobby_id_series.sample(
                size, random_state=rng, ignore_index=True)
            interested = rng.random(size) > 0.5
            ratings = rng.integers(0, 6, size=size)

            dummy_data = pd.DataFrame(
                {
                    "user_id": uuid4(),
                    "hobby_id": hobby_ids,
                    "interested": interested,
                    "rating": ratings,
                }
            )
            content.append(dummy_data)

        return pd.concat(content, ignore_index=True)


user_hobby_recommender = _UserHobbyRecommender()
