"""Module containing starship crawler."""
import re
from typing import List, Optional

from requests_html import HTMLSession

from starships.config.config import Config
from starships.config.logger import LOGGER
from starships.extensions import SESSION
from starships.models import Starship

_RE = re.compile("Class \\d*\\.?\\d+")
_DB_SESSION = SESSION()


def get_starships() -> List[Starship]:
    """Return a list of retrieved starships."""
    html_session = HTMLSession()
    response = html_session.get(Config().DATABANK_URL)

    starship_table = response.html.find('a[title="Starship"]+ul')[0]
    starship_urls = {
        e.attrs["title"]: e.absolute_links.pop() for e in starship_table.find("a")
    }

    starships_list = []

    for starship_name, starship_url in starship_urls.items():
        hyperdrive_rating = _get_hypedrive_rating(html_session, starship_url)
        if hyperdrive_rating:
            starships_list.append(
                Starship(name=starship_name, hyperdrive_rating=hyperdrive_rating)
            )

    return starships_list


def _get_hypedrive_rating(session: HTMLSession, starship_url: str) -> Optional[float]:
    """Visit each URL and return hyperdrive rating for given vehicle url."""
    response_url = session.get(starship_url)
    hyperdrive = response_url.html.find("[data-source=hyperdrive] li", first=True)

    if hyperdrive:
        return _format_hyperdrive_rating(hyperdrive.text)

    return None


def _format_hyperdrive_rating(text: str) -> float:
    """Return float number hyperdrive rating parsed from string."""
    return float(_RE.search(str(text)).group().lstrip("Class "))  # type: ignore


def crawl_starships() -> None:
    """
    Fetch and save starships to the database.

    Extracted for unit tests purposes.
    """
    try:
        if _DB_SESSION.query(Starship).first():
            LOGGER.info("The `starships` table is already populated: skipping crawling")
            exit(0)

        LOGGER.info("Started starships crawling")
        starships = get_starships()
        LOGGER.info(f"Finished starships crawling. Found starships: {starships}")

        LOGGER.info("Saving starships to the database")
        _DB_SESSION.add_all(starships)
        _DB_SESSION.commit()
        LOGGER.info("Finished saving starships to the database")

        exit(0)

    except Exception:
        LOGGER.exception("There was an error during crawling")
        exit(1)


if __name__ == "__main__":
    crawl_starships()
