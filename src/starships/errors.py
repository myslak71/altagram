"""Application errors."""
from werkzeug.exceptions import BadRequest


class ValidationError(BadRequest):
    """Raised when request data is invalid."""
