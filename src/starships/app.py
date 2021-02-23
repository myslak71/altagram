"""Flask app factory module."""
from flask import Flask

from starships.extensions import BLUEPRINT, DB, RESTFUL_API, SESSION
from starships.urls import urls

extensions = (DB, RESTFUL_API)

session = SESSION()

for view, url in urls:
    RESTFUL_API.add_resource(view, url)


def create_app() -> Flask:
    """
    Initialize and return Flask app instance.

    Load the configuration, initialize extensions and register blueprints.
    """
    app = Flask(__name__)
    app.config.from_object("starships.config.config.CONFIG")

    for extension in extensions:
        extension.init_app(app)

    app.register_blueprint(BLUEPRINT)

    return app
