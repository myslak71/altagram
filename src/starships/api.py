"""Starship API module."""
from http import HTTPStatus
from typing import Dict, Tuple, Union

from flask_restful import Api

from starships.config.logger import LOGGER
from starships.errors import ValidationError


class StarshipsApi(Api):
    """
    Flask-restful custom api class.

    Overrides error default handling with custom error response structure.
    """

    def handle_error(
        self, exception: Exception
    ) -> Tuple[Dict[str, Union[int, str]], int]:
        """
        Return appropriate error message depending on passed exception.

        Log exception and return BadRequest for `ValidationError` and
        `InternalServerError` for other exceptions.
        """
        LOGGER.debug(str(exception))
        if isinstance(exception, ValidationError):
            return {
                "code": HTTPStatus.BAD_REQUEST,
                "name": HTTPStatus.BAD_REQUEST.phrase,
                "description": exception.description,
            }, HTTPStatus.BAD_REQUEST

        LOGGER.error(str(exception))
        return {
            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "name": HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            "description": "Unknown error has occurred",
        }, HTTPStatus.INTERNAL_SERVER_ERROR
