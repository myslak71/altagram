"""Test configuration module and tests fixtures."""

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.orm import Session

from starships.app import create_app
from starships.extensions import DB, SESSION
from starships.models import Starship


@pytest.fixture()
def alembic_config() -> Config:
    """Return alembic config for migrations."""
    return Config("alembic.ini")


@pytest.fixture
def migrate_db(alembic_config) -> None:
    """Apply migrations to the database."""
    command.upgrade(alembic_config, "head")


@pytest.fixture
def db_session() -> Session:
    """Return db session."""
    app = create_app()
    DB.app = app
    yield SESSION


@pytest.fixture
def client(db_session, migrate_db, alembic_config):
    """Fixtures which creates and yields flask test_client."""
    app = create_app()

    yield app.test_client()

    db_session.query(Starship).delete()
    db_session.commit()
    command.downgrade(alembic_config, "-1")


@pytest.fixture
def starships_fixture(db_session):
    """Save and return starships in the database."""
    starships = [
        Starship(name=f"Starship no. {i+1}", hyperdrive_rating=i + 1)
        for i in range(0, 30)
    ]
    db_session.add_all(starships)
    db_session.commit()
