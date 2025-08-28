from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class HobbyBase(SQLModel):
    """Shared Hobby props"""
    name: str = Field(index=True, unique=True, min_length=2)
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
