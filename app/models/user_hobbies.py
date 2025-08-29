from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

from . import User, Hobby


class UserHobbyBase(SQLModel):
    """Shared UserHobby props"""
    interested: bool = True
    rating: int | None = None
    # todo: rating defaults to 0, user choice from 1-5


class UserHobbyLink(UserHobbyBase, table=True):
    """DB model for userhobbylink table"""
    __tablename__ = "user_hobbies"

    user_id: UUID = Field(foreign_key="users.id",
                          primary_key=True, ondelete="CASCADE")
    hobby_id: UUID = Field(foreign_key="hobbies.id",
                           primary_key=True, ondelete="CASCADE")

    user: User = Relationship(back_populates="hobby_links")
    hobby: Hobby = Relationship()


class UserHobbyPublic(UserHobbyBase):
    """Props to return for UserHobby"""
    user_id: UUID
    hobby_id: UUID


class UserHobbyCreate(UserHobbyBase):
    """Props to receive on UserHobby creation"""
    hobby_id: UUID


class UserHobbyUpdate(UserHobbyBase):
    """Props to receive on UserHobby update"""
    pass


def get_metadata():
    return SQLModel.metadata
