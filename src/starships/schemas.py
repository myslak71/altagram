"""Schemas module. Contains serializing schemas fo database models."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from starships.extensions import SESSION
from starships.models import Starship


class BaseSchema(SQLAlchemyAutoSchema):
    """Base schema for all database models."""

    class Meta:
        sqla_session = SESSION


class StarshipSchema(BaseSchema):
    """Starship serializing schema."""

    class Meta(BaseSchema.Meta):
        model = Starship
        dump_only = ("name", "hyperdrive_rating")
