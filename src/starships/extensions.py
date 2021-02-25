"""
Flask extensions module.

Contains extensions variables used in the application initialization.
"""
from flask import Blueprint
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from starships.api import StarshipsApi
from starships.config.config import CONFIG

ENGINE = create_engine(
    CONFIG.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)
SESSION_FACTORY = sessionmaker(bind=ENGINE, query_cls=BaseQuery)
SESSION = scoped_session(SESSION_FACTORY)

DB = SQLAlchemy()

BLUEPRINT = Blueprint("api", "starships.app")
RESTFUL_API = StarshipsApi(BLUEPRINT)
