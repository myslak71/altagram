"""Spaceship database model module."""
from sqlalchemy import Column, Float, String

from starships.extensions import DB


class Starship(DB.Model):
    """Spaceship database model."""

    __tablename__ = "starships"

    name = Column(String, primary_key=True)
    hyperdrive_rating = Column(Float, primary_key=True)

    def __repr__(self) -> str:
        """Return object representation."""
        return (
            f'Starship(name="{self.name}", hyperdrive_rating={self.hyperdrive_rating}'
        )

    def __eq__(self, other) -> bool:
        """Compare starships field by field."""
        return (
            self.name == other.name
            and self.hyperdrive_rating == other.hyperdrive_rating
        )
