from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4


# User models

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

    hobby_links: list["UserHobbyLink"] = Relationship(back_populates="user")


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


# Hobby models

class HobbyBase(SQLModel):
    """Shared Hobby props"""
    name: str = Field(index=True, unique=True)
    description: str | None = None


class Hobby(HobbyBase, table=True):
    """DB model for hobby table"""
    __tablename__ = "hobbies"

    id: UUID = Field(default_factory=uuid4, primary_key=True)


class HobbyPublic(HobbyBase):
    """Props to return for Hobby"""
    id: UUID


class HobbyCreate(HobbyBase):
    """Props to receive on Hobby creation"""
    pass


class HobbyUpdate(HobbyBase):
    """Props to receive on Hobby update"""
    pass


# UserHobby models

class UserHobbyBase(SQLModel):
    """Shared UserHobby props"""
    interested: bool = True
    rating: int | None = None


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
