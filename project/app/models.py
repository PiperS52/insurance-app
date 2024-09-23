from typing import Optional
from sqlmodel import SQLModel, Field


class PolicyBase(SQLModel):
    """pydantic model"""

    title: str
    date: str
    type: str
    name: str
    wording: str
    price: float


class Policy(PolicyBase, table=True):
    """policy db model"""

    id: int = Field(default=None, primary_key=True)

    class Config:
        from_attributes = True
