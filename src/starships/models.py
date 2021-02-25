"""Spaceship database model module."""
from typing import TypeVar

from sqlalchemy import Column, Float, String

from starships.extensions import DB

StarshipType = TypeVar("StarshipType", bound="Starship")


class Starship(DB.Model):
    """Spaceship database model."""

    __tablename__ = "starships"

    name = Column(String, primary_key=True)
    hyperdrive_rating = Column(Float)

    def __repr__(self) -> str:
        """Return object representation."""
        return (
            f'Starship(name="{self.name}", hyperdrive_rating={self.hyperdrive_rating}'
        )

    def __eq__(self, other: StarshipType) -> bool:  # type: ignore
        """Compare starships field by field."""
        return (
            self.name == other.name
            and self.hyperdrive_rating == other.hyperdrive_rating
        )
