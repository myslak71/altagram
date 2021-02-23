"""Starship crawler test module."""
from http import HTTPStatus
from unittest.mock import patch

import pytest
import responses

from starships import crawler
from starships.crawler import crawl_starships, get_starships
from starships.models import Starship


@responses.activate
def test_get_starships(databank_page, starship1_page, starship2_page):
    """Test if correct starships are returned for successful responses."""
    responses.add(
        responses.GET,
        "https://starwars.fandom.com/wiki/Databank_(website)",
        body=databank_page,
        status=HTTPStatus.OK,
        content_type="text/html",
    )
    responses.add(
        responses.GET,
        "https://starwars.fandom.com/wiki/Starship1",
        body=starship1_page,
        status=HTTPStatus.OK,
        content_type="text/html",
    )
    responses.add(
        responses.GET,
        "https://starwars.fandom.com/wiki/Starship2",
        body=starship2_page,
        status=HTTPStatus.OK,
        content_type="text/html",
    )

    assert get_starships() == [
        Starship(name="Starship1", hyperdrive_rating=1.5),
        Starship(name="Starship2", hyperdrive_rating=5.0),
    ]


@patch.object(crawler, "_DB_SESSION")
@patch("starships.crawler.get_starships")
def test_crawl_starships(get_starships_mock, session_mock):
    """Test if no error occurs for valid responses."""
    session_mock.query.return_value.first.return_value = False
    with pytest.raises(SystemExit) as exception:
        crawl_starships()
    assert exception.type == SystemExit
    assert exception.value.code == 0


@patch.object(crawler, "_DB_SESSION")
@patch("starships.crawler.get_starships")
def test_crawl_starships_exception(get_starships_mock, session_mock):
    """Test if system exit with error code for occurring exception."""
    session_mock.query.return_value.first.return_value = False
    get_starships_mock.side_effect = Exception
    with pytest.raises(SystemExit) as exception:
        crawl_starships()
    assert exception.type == SystemExit
    assert exception.value.code == 1
