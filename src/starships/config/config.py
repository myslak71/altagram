"""Module which stores configurations for development and tests."""
from typing import Optional

from pydantic import BaseSettings
from sqlalchemy.engine.url import URL


class Config(BaseSettings):
    """
    Application config class.

    Attributes are fetched from environment variables during app initialization.
    """

    ENV: Optional[str] = "production"
    DEVELOPMENT: Optional[bool] = True

    DB_USER: Optional[str] = "postgres"
    DB_PASSWORD: Optional[str] = "postgres"
    DB_HOST: Optional[str] = "altagram-db"
    DB_PORT: Optional[str] = "5432"
    DB_NAME: Optional[str] = "altagram"

    DATABANK_URL: Optional[str] = "https://starwars.fandom.com/wiki/Databank_(website)"

    DEFAULT_PAGE_NUMBER: Optional[int] = 1
    DEFAULT_PAGE_SIZE: Optional[int] = 10

    SQLALCHEMY_DATABASE_URI: Optional[URL] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False  # disables pytest warning

    def __init__(self, *args, **kwargs) -> None:
        """Set `SQLALCHEMY_DATABASE_URI` to disable pytest warning."""
        super().__init__(*args, **kwargs)
        self.SQLALCHEMY_DATABASE_URI = URL(
            drivername="postgresql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


CONFIG = Config()
