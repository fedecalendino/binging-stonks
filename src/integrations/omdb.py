import logging
import os
import re

import requests

from classes import Show

LOGGER = logging.getLogger("omdb")

API_KEY = os.getenv("OMDB_API_KEY", "YOUR-API-KEY")
API_URL = "http://www.omdbapi.com/?"

IMDB_ID_REGEX = re.compile(r"tt\d+")


def search(search_content: str) -> Show:
    if API_KEY in [None, "", "YOUR-API-KEY"]:
        LOGGER.error("A valid api key for OMDB is required")
        exit(1)

    LOGGER.info("")
    LOGGER.info("Searching for %s in OMDB", search_content)

    search_content = search_content.lower()
    search_type = "i" if IMDB_ID_REGEX.match(search_content) else "t"

    params = {
        "type": "series",
        "apikey": API_KEY,
        search_type: search_content
    }

    data = requests.get(url=API_URL, params=params).json()
    imdb_id = data["imdbID"]

    LOGGER.info("Found result with imdb_id '%s'", imdb_id)

    show = Show(
        imdb_id=imdb_id,
        title=data["Title"],
        seasons=int(data["totalSeasons"]),
    )

    show.plot = data.get("Plot", "No plot found")
    show.year = int(data["Released"][-4:])
    show.poster = data.get("Poster")
    show.rating = float(data.get("imdbRating", 0.0))
    show.votes = int(re.sub(r"[^\d]", "", data.get("imdbVotes", "0")))

    return show
