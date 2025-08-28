from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # type-only imports to satisfy type checkers
    from . import UserHobbyLink


class UserBase(SQLModel):
    """Shared User props"""
    username: str = Field(unique=True, index=True)
    email: str | None = Field(default=None, unique=True)
    name: str


class User(UserBase, table=True):
    """DB model for user table"""
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str

    hobby_links: list["UserHobbyLink"] = Relationship(
        back_populates="user", passive_deletes="all")


class UserPublic(UserBase):
    """Props to return for User"""
    id: UUID


class UserCreate(UserBase):
    """Props to receive on User creation"""
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    """Props to receive on User update"""
    username: str | None = None  # type: ignore
    name: str | None = None  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)
