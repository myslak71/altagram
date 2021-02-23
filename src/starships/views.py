"""Starship resources module."""
from typing import Dict, Union

from flask import current_app as app
from flask import request
from flask_restful import Resource
from sqlalchemy import text

from starships.errors import ValidationError
from starships.extensions import SESSION
from starships.models import Starship
from starships.pagination import paginate
from starships.schemas import StarshipSchema

session = SESSION()


class StarshipResource(Resource):
    """Starship API resource."""

    model = Starship
    allowed_sort_columns = StarshipSchema.Meta.dump_only
    allowed_sort_orders = ("asc", "desc")

    def get(self) -> Dict[str, Union[int, Dict[str, Union[int, str]], str]]:
        """Return paginated starships."""
        self._validate_pagination_args()
        self._validate_sort_args()

        sort_by = request.args.get("sort_by")
        order_by = request.args.get("order_by", "desc")

        query = session.query(Starship)

        if sort_by:
            query = query.order_by(
                text(f"{self.model.__tablename__}.{sort_by} {order_by}")
            )

        return paginate(query, StarshipSchema())

    @staticmethod
    def _validate_pagination_args() -> None:
        """
        Validate pagination query arguments.

        Raise `ValidationError` if passed pagination query arguments
        can't be cast to integer or are lower than `1`.
        """
        msg = "`{}` has to be a positive integer"

        try:
            page = int(request.args.get("page", app.config["DEFAULT_PAGE_NUMBER"]))
        except ValueError as exception:
            raise ValidationError(msg.format("page")) from exception

        if page < 1:
            raise ValidationError(msg.format("page"))

        try:
            page_size = int(
                request.args.get("page_size", app.config["DEFAULT_PAGE_SIZE"])
            )
        except ValueError as exception:
            raise ValidationError(msg.format("page_size")) from exception

        if page_size < 1:
            raise ValidationError(msg.format("page_size"))

    def _validate_sort_args(self) -> None:
        """
        Validate sort query arguments.

        Raise `ValidationError` if passed sort query arguments
        aren't allowed.
        """
        sort_by = request.args.get("sort_by")
        if sort_by and sort_by not in self.allowed_sort_columns:
            raise ValidationError(
                f"`sort_by` needs to be one of {self.allowed_sort_columns}"
            )

        order_by = request.args.get("order_by", "desc")
        if order_by and order_by not in self.allowed_sort_orders:
            raise ValidationError(
                f"`sort_by` needs to be one of {self.allowed_sort_orders}"
            )
