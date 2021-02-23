"""Query pagination module."""
from typing import Dict, Optional, Union

import flask_sqlalchemy
from flask import current_app as app
from flask import request, url_for

from starships.schemas import BaseSchema


def paginate(
    query: flask_sqlalchemy.BaseQuery, schema: BaseSchema
) -> Dict[str, Union[int, Dict[str, Union[int, str]], str, None]]:
    """Return paginated BaseQuery result."""
    page = int(request.args.get("page", app.config["DEFAULT_PAGE_NUMBER"]))
    per_page = int(request.args.get("page_size", app.config["DEFAULT_PAGE_SIZE"]))

    page_obj = query.paginate(page=page, per_page=per_page)

    sort_args = {
        "sort_by": request.args.get("sort_by"),
        "order_by": request.args.get("order_by"),
    }

    if page_obj.has_next:
        next_page: Optional[str] = url_for(
            request.endpoint,  # type: ignore
            page=page_obj.next_num,
            per_page=per_page,
            **request.view_args,
            **sort_args
        )
    else:
        next_page = None

    if page_obj.has_prev:
        prev_page: Optional[str] = url_for(
            request.endpoint,  # type: ignore
            page=page_obj.prev_num,
            per_page=per_page,
            **request.view_args,
            **sort_args
        )
    else:
        prev_page = None

    return {
        "count": page_obj.total,
        "pages": page_obj.pages,
        "next": next_page,
        "prev": prev_page,
        "results": schema.dump(page_obj.items, many=True),
    }
