"""
Manual smoke-test for CensusConfig. Run from the ingestion/ directory:

    python debug_census.py

Exercises the pieces of census.py that exist so far (grouping + raw API
fetches) and logs what comes back, without touching SQLite. Prints to the
console and writes the same output to debug_census.log.
"""

import logging
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from sources.census import CensusConfig

RETRIES = 3


def get_with_retries(url):
    """The Census API intermittently 404s on valid requests; retry a few times."""
    for attempt in range(1, RETRIES + 1):
        response = requests.get(url)
        if response.ok:
            return response
        log.warning(
            "GET failed (attempt %d/%d): %s %s", attempt, RETRIES, response.status_code, url
        )
        time.sleep(1)
    response.raise_for_status()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / "debug_census.log", mode="w"),
    ],
)
log = logging.getLogger("debug_census")


def find_place_fips(config):
    """
    One-off lookup: queries NAME + place for every place in each target
    state, so PLACE_FIPS values come straight from the same dataset
    fetch_detail/fetch_subject use, instead of a different code scheme.
    """
    log.info("=== Resolving place FIPS codes by NAME ===")
    for state_fips, cities in config._group_cities_by_state().items():
        url = f"{config.base_url_detail}?get=NAME&for=place:*&in=state:{state_fips}&key={config.api_key}"
        response = get_with_retries(url)
        header, body = response.json()[0], response.json()[1:]
        rows = [dict(zip(header, row)) for row in body]

        for city in cities:
            matches = [r for r in rows if r["NAME"].startswith(city)]
            log.info("'%s' (state_fips=%s) candidates: %s", city, state_fips, matches)


def main():
    config = CensusConfig()
    find_place_fips(config)

    log.info("=== merge() output (one line per city, ready for table insertion) ===")
    for city, detail_row, subject_row in config.merge():
        log.info("'%s' detail_row=%s", city, detail_row)
        log.info("'%s' subject_row=%s", city, subject_row)


if __name__ == "__main__":
    main()
