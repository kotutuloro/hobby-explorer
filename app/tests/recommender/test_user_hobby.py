import pytest
import pandas as pd
import numpy as np
from uuid import uuid4, UUID
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.engine import Connectable

from app.recommender.user_hobby import _UserHobbyRecommender
from app.models import Hobby, UserHobbyLink


class TestUserHobbyRecommender:
    @pytest.fixture
    def recommender(self) -> _UserHobbyRecommender:
        """Create a fresh recommender instance for each test"""
        return _UserHobbyRecommender()

    @pytest.fixture
    def sample_user_hobby_data(self) -> pd.DataFrame:
        """Create sample user-hobby data for testing"""
        user_ids = [uuid4() for _ in range(3)]
        hobby_ids = [uuid4() for _ in range(5)]

        data = []
        for user_id in user_ids:
            for hobby_id in hobby_ids:
                data.append({
                    "user_id": user_id,
                    "hobby_id": hobby_id,
                    "interested": True,
                    "rating": np.random.randint(0, 6)
                })

        return pd.DataFrame(data)

    @pytest.fixture
    def sample_hobby_data(self):
        """Create sample hobby data for testing"""
        return pd.DataFrame({
            "id": [uuid4() for _ in range(5)]
        })

    def test_load_from_sql_with_dummy_data(self, recommender, sample_user_hobby_data, sample_hobby_data):
        mock_conn = Mock(spec=Connectable)
        with patch('pandas.read_sql_table') as mock_read_sql:
            mock_read_sql.side_effect = [
                sample_user_hobby_data, sample_hobby_data]
            recommender.load_from_sql(mock_conn)

            assert recommender._user_hobby_matrix is not None
            assert recommender._user_similarity_df is not None
            assert recommender._hobby_similarity_df is not None

            # Verify dummy data was added
            assert len(recommender._user_hobby_matrix) >= 100

    def test_load_from_sql_without_dummy_data(self, recommender, sample_user_hobby_data, sample_hobby_data):
        mock_conn = Mock(spec=Connectable)
        with patch('pandas.read_sql_table') as mock_read_sql:
            mock_read_sql.side_effect = [
                sample_user_hobby_data, sample_hobby_data]
            recommender.load_from_sql(mock_conn, include_dummy=False)

            assert recommender._user_hobby_matrix is not None
            assert recommender._user_similarity_df is not None
            assert recommender._hobby_similarity_df is not None

            # Verify no dummy data was added
            assert len(recommender._user_hobby_matrix) == 3

    def test_load_from_sql_no_dummy_when_enough_data(self, recommender):
        mock_conn = Mock(spec=Connectable)

        # Create data with more than 50 entries
        user_ids = [uuid4() for _ in range(10)]
        hobby_ids = [uuid4() for _ in range(6)]
        sample_data = []
        for user_id in user_ids:
            for hobby_id in hobby_ids:
                sample_data.append({
                    "user_id": user_id,
                    "hobby_id": hobby_id,
                    "interested": True,
                    "rating": 5
                })

        with patch('pandas.read_sql_table') as mock_read_sql:
            mock_read_sql.return_value = pd.DataFrame(sample_data)
            recommender.load_from_sql(mock_conn, include_dummy=True)

            # Verify no dummy data was added
            assert len(recommender._user_hobby_matrix) == 10

    def test_analyze_ratings_creates_matrices(self, recommender, sample_user_hobby_data):
        """Test that _analyze_ratings creates all required matrices"""
        recommender._analyze_ratings(sample_user_hobby_data)

        assert recommender._user_hobby_matrix is not None
        assert isinstance(recommender._user_hobby_matrix, pd.DataFrame)
        assert len(recommender._user_hobby_matrix) == 3  # 3 users
        assert len(recommender._user_hobby_matrix.columns) == 5  # 5 hobbies

        assert recommender._user_similarity_df is not None
        assert isinstance(recommender._user_similarity_df, pd.DataFrame)
        assert recommender._user_similarity_df.shape == (3, 3)  # 3x3 matrix

        assert recommender._hobby_similarity_df is not None
        assert isinstance(recommender._hobby_similarity_df, pd.DataFrame)
        assert recommender._hobby_similarity_df.shape == (5, 5)  # 5x5 matrix

    def test_get_hobby_recs_for_user_success(self, recommender, sample_user_hobby_data):
        user_id = sample_user_hobby_data["user_id"].iat[0]
        recommender._analyze_ratings(sample_user_hobby_data)
        recs = recommender.get_hobby_recs_for_user(user_id, num_recs=3)

        assert isinstance(recs, list)
        assert len(recs) <= 3
        assert all(isinstance(rec, UUID) for rec in recs)

    def test_get_hobby_recs_for_user_missing_data_raises(self, recommender):
        with pytest.raises(AttributeError, match="Missing required dataframe attributes"):
            # call without loading first
            recommender.get_hobby_recs_for_user(uuid4())

    def test_get_similar_hobbies_success(self, recommender, sample_user_hobby_data):
        hobby_id = sample_user_hobby_data["hobby_id"].iloc[0]
        recommender._analyze_ratings(sample_user_hobby_data)
        similar = recommender.get_similar_hobbies(hobby_id, num_recs=2)

        assert isinstance(similar, list)
        assert len(similar) <= 2
        assert all(isinstance(hobby, UUID) for hobby in similar)

    def test_get_similar_hobbies_missing_data_raises(self, recommender):
        with pytest.raises(AttributeError, match="Missing required dataframe attributes"):
            # call without loading first
            recommender.get_similar_hobbies(uuid4())

    def test_dummy_user_hobby_data_generation(self):
        hobby_ids = pd.Series([uuid4() for _ in range(10)])
        dummy_data = _UserHobbyRecommender._dummy_user_hobby_data(hobby_ids)

        # Verify dummy data structure
        assert isinstance(dummy_data, pd.DataFrame)
        assert "user_id" in dummy_data.columns
        assert "hobby_id" in dummy_data.columns
        assert "interested" in dummy_data.columns
        assert "rating" in dummy_data.columns

        # Verify data types and ranges
        assert all(isinstance(uid, UUID) for uid in dummy_data["user_id"])
        assert all(isinstance(hid, UUID) for hid in dummy_data["hobby_id"])
        assert all(isinstance(interested, bool)
                   for interested in dummy_data["interested"])
        assert all(0 <= rating <= 5 for rating in dummy_data["rating"])

        # Verify each user has 1-20 hobbies
        user_hobby_counts = dummy_data.groupby("user_id").size()
        assert all(1 <= count <= 20 for count in user_hobby_counts)

    def test_dummy_data_deterministic(self):
        """Test that dummy data generation is deterministic with same seed"""
        hobby_ids = pd.Series([uuid4() for _ in range(5)])
        dummy_data_1 = _UserHobbyRecommender._dummy_user_hobby_data(hobby_ids)
        dummy_data_2 = _UserHobbyRecommender._dummy_user_hobby_data(hobby_ids)

        # The structure and ratings should be identical, but user_ids will be different
        # since they're randomly generated UUIDs
        assert dummy_data_1.shape == dummy_data_2.shape
        assert len(dummy_data_1) == len(dummy_data_2)

        pd.testing.assert_series_equal(
            dummy_data_1["rating"],
            dummy_data_2["rating"],
            check_names=False
        )
        pd.testing.assert_series_equal(
            dummy_data_1["interested"],
            dummy_data_2["interested"],
            check_names=False
        )
        pd.testing.assert_series_equal(
            dummy_data_1["hobby_id"],
            dummy_data_2["hobby_id"],
            check_names=False
        )

    def test_cosine_similarity_calculation(self, recommender):
        data = pd.DataFrame([
            {"user_id": "user1", "hobby_id": "hobby1", "rating": 5},
            {"user_id": "user1", "hobby_id": "hobby2", "rating": 2},
            {"user_id": "user2", "hobby_id": "hobby1", "rating": 5},
            {"user_id": "user2", "hobby_id": "hobby2", "rating": 2},
        ])
        recommender._analyze_ratings(data)

        # User similarity should be 1.0 for identical rating patterns
        user_sim = recommender._user_similarity_df.loc["user1", "user2"]
        assert abs(user_sim - 1.0) < 1e-10

        # Hobby similarity should be 1.0 for identical user patterns
        hobby_sim = recommender._hobby_similarity_df.loc["hobby1", "hobby2"]
        assert abs(hobby_sim - 1.0) < 1e-10
