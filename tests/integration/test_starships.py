"""Starship views integration tests."""
import json
from unittest.mock import patch

import pytest


def test_starships_empty_database(
    client,
):
    """Test if valid response is returned for empty database."""
    response = client.get("/starships/")

    assert response.status_code == 200
    assert json.loads(response.data) == {
        "count": 0,
        "pages": 0,
        "next": None,
        "prev": None,
        "results": [],
    }


def test_starships_no_querystring(client, starships_fixture):
    """Test if default pagination values are returned for no querystring request."""
    response = client.get("/starships/")

    assert response.status_code == 200
    assert json.loads(response.data) == {
        "count": 30,
        "pages": 3,
        "next": "/starships/?page=2&per_page=10",
        "prev": None,
        "results": [
            {"hyperdrive_rating": 1.0, "name": "Starship no. 1"},
            {"hyperdrive_rating": 2.0, "name": "Starship no. 2"},
            {"hyperdrive_rating": 3.0, "name": "Starship no. 3"},
            {"hyperdrive_rating": 4.0, "name": "Starship no. 4"},
            {"hyperdrive_rating": 5.0, "name": "Starship no. 5"},
            {"hyperdrive_rating": 6.0, "name": "Starship no. 6"},
            {"hyperdrive_rating": 7.0, "name": "Starship no. 7"},
            {"hyperdrive_rating": 8.0, "name": "Starship no. 8"},
            {"hyperdrive_rating": 9.0, "name": "Starship no. 9"},
            {"hyperdrive_rating": 10.0, "name": "Starship no. 10"},
        ],
    }


@pytest.mark.parametrize(
    "querystring, expected_data",
    (
        (
            "page=1&per_page=10",
            {
                "count": 30,
                "pages": 3,
                "next": "/starships/?page=2&per_page=10",
                "prev": None,
                "results": [
                    {"hyperdrive_rating": 1.0, "name": "Starship no. 1"},
                    {"hyperdrive_rating": 2.0, "name": "Starship no. 2"},
                    {"hyperdrive_rating": 3.0, "name": "Starship no. 3"},
                    {"hyperdrive_rating": 4.0, "name": "Starship no. 4"},
                    {"hyperdrive_rating": 5.0, "name": "Starship no. 5"},
                    {"hyperdrive_rating": 6.0, "name": "Starship no. 6"},
                    {"hyperdrive_rating": 7.0, "name": "Starship no. 7"},
                    {"hyperdrive_rating": 8.0, "name": "Starship no. 8"},
                    {"hyperdrive_rating": 9.0, "name": "Starship no. 9"},
                    {"hyperdrive_rating": 10.0, "name": "Starship no. 10"},
                ],
            },
        ),
        (
            "page=2&per_page=10",
            {
                "count": 30,
                "pages": 3,
                "next": "/starships/?page=3&per_page=10",
                "prev": "/starships/?page=1&per_page=10",
                "results": [
                    {"hyperdrive_rating": 11.0, "name": "Starship no. 11"},
                    {"hyperdrive_rating": 12.0, "name": "Starship no. 12"},
                    {"hyperdrive_rating": 13.0, "name": "Starship no. 13"},
                    {"hyperdrive_rating": 14.0, "name": "Starship no. 14"},
                    {"hyperdrive_rating": 15.0, "name": "Starship no. 15"},
                    {"hyperdrive_rating": 16.0, "name": "Starship no. 16"},
                    {"hyperdrive_rating": 17.0, "name": "Starship no. 17"},
                    {"hyperdrive_rating": 18.0, "name": "Starship no. 18"},
                    {"hyperdrive_rating": 19.0, "name": "Starship no. 19"},
                    {"hyperdrive_rating": 20.0, "name": "Starship no. 20"},
                ],
            },
        ),
        (
            "page=3&per_page=10",
            {
                "count": 30,
                "pages": 3,
                "next": None,
                "prev": "/starships/?page=2&per_page=10",
                "results": [
                    {"hyperdrive_rating": 21.0, "name": "Starship no. 21"},
                    {"hyperdrive_rating": 22.0, "name": "Starship no. 22"},
                    {"hyperdrive_rating": 23.0, "name": "Starship no. 23"},
                    {"hyperdrive_rating": 24.0, "name": "Starship no. 24"},
                    {"hyperdrive_rating": 25.0, "name": "Starship no. 25"},
                    {"hyperdrive_rating": 26.0, "name": "Starship no. 26"},
                    {"hyperdrive_rating": 27.0, "name": "Starship no. 27"},
                    {"hyperdrive_rating": 28.0, "name": "Starship no. 28"},
                    {"hyperdrive_rating": 29.0, "name": "Starship no. 29"},
                    {"hyperdrive_rating": 30.0, "name": "Starship no. 30"},
                ],
            },
        ),
    ),
)
def test_starships(
    client,
    starships_fixture,
    querystring,
    expected_data,
):
    """Test if proper results are returned while pagination arguments are passed."""
    response = client.get(f"/starships/?{querystring}")

    assert response.status_code == 200
    assert json.loads(response.data) == expected_data


@pytest.mark.parametrize(
    "order_by, expected_data",
    (
        (
            "desc",
            {
                "count": 30,
                "pages": 3,
                "next": (
                    "/starships/"
                    "?page=2&per_page=10&sort_by=hyperdrive_rating&order_by=desc"
                ),
                "prev": None,
                "results": [
                    {"name": "Starship no. 30", "hyperdrive_rating": 30.0},
                    {"name": "Starship no. 29", "hyperdrive_rating": 29.0},
                    {"name": "Starship no. 28", "hyperdrive_rating": 28.0},
                    {"name": "Starship no. 27", "hyperdrive_rating": 27.0},
                    {"name": "Starship no. 26", "hyperdrive_rating": 26.0},
                    {"name": "Starship no. 25", "hyperdrive_rating": 25.0},
                    {"name": "Starship no. 24", "hyperdrive_rating": 24.0},
                    {"name": "Starship no. 23", "hyperdrive_rating": 23.0},
                    {"name": "Starship no. 22", "hyperdrive_rating": 22.0},
                    {"name": "Starship no. 21", "hyperdrive_rating": 21.0},
                ],
            },
        ),
        (
            "asc",
            {
                "count": 30,
                "pages": 3,
                "next": (
                    "/starships/"
                    "?page=2&per_page=10&sort_by=hyperdrive_rating&order_by=asc"
                ),
                "prev": None,
                "results": [
                    {"name": "Starship no. 1", "hyperdrive_rating": 1.0},
                    {"name": "Starship no. 2", "hyperdrive_rating": 2.0},
                    {"name": "Starship no. 3", "hyperdrive_rating": 3.0},
                    {"name": "Starship no. 4", "hyperdrive_rating": 4.0},
                    {"name": "Starship no. 5", "hyperdrive_rating": 5.0},
                    {"name": "Starship no. 6", "hyperdrive_rating": 6.0},
                    {"name": "Starship no. 7", "hyperdrive_rating": 7.0},
                    {"name": "Starship no. 8", "hyperdrive_rating": 8.0},
                    {"name": "Starship no. 9", "hyperdrive_rating": 9.0},
                    {"name": "Starship no. 10", "hyperdrive_rating": 10.0},
                ],
            },
        ),
    ),
)
def test_starships_order(client, starships_fixture, order_by, expected_data):
    """Test if starships are returned in appropriate order."""
    response = client.get(f"/starships/?sort_by=hyperdrive_rating&order_by={order_by}")

    assert response.status_code == 200
    assert json.loads(response.data) == expected_data


def test_starships_invalid_order_by(
    client,
):
    """Test if appropriate error message is returned for invalid `order_by`."""
    response = client.get("/starships/?sort_by=hyperdrive_rating&order_by=brooklyn")

    assert response.status_code == 400
    assert json.loads(response.data) == {
        "code": 400,
        "description": "`sort_by` needs to be one of ('asc', 'desc')",
        "name": "Bad Request",
    }


def test_starships_invalid_sort_by(
    client,
):
    """Test if appropriate error message is returned for invalid `sort_by`."""
    response = client.get("/starships/?sort_by=brooklyn")

    assert response.status_code == 400
    assert json.loads(response.data) == {
        "code": 400,
        "description": "`sort_by` needs to be one of ('name', 'hyperdrive_rating')",
        "name": "Bad Request",
    }


@pytest.mark.parametrize(
    "page,",
    ("invalid_page", -10),
)
def test_starships_invalid_page(client, page):
    """Test if appropriate error message is returned for invalid `page`."""
    response = client.get(f"/starships/?page={page}")

    assert response.status_code == 400
    assert json.loads(response.data) == {
        "code": 400,
        "description": "`page` has to be a positive integer",
        "name": "Bad Request",
    }


@pytest.mark.parametrize(
    "page_size,",
    ("invalid_page_size", -10),
)
def test_starships_invalid_page_size(client, page_size):
    """Test if appropriate error message is returned for invalid `page_size`."""
    response = client.get(f"/starships/?page_size={page_size}")

    assert response.status_code == 400
    assert json.loads(response.data) == {
        "code": 400,
        "description": "`page_size` has to be a positive integer",
        "name": "Bad Request",
    }


@patch("starships.views.paginate")
def test_starships_unknown_error(pagination_mock, client):
    """Test if appropriate error message is returned for invalid `page_size`."""
    pagination_mock.side_effects = ValueError
    response = client.get("/starships/")

    assert response.status_code == 500
    assert json.loads(response.data) == {
        "code": 500,
        "description": "Unknown error has occurred",
        "name": "Internal Server Error",
    }
