import logging
from itertools import count

import requests
from bs4 import BeautifulSoup as Soup

from classes import Show, Episode

LOGGER = logging.getLogger("imdb")


def scrap(show: Show) -> Show:
    LOGGER.info("")
    LOGGER.info("Looking for episodes of %s", show.title)

    index = count(start=1)

    for season_number in range(1, show.season_count + 1):
        season_url = f'{show.url}/episodes?season={season_number}'

        content = requests.get(season_url)
        soup = Soup(content.text, features="html.parser")

        for div in soup.find_all('div', {'class': 'list_item'}):
            div = div.find('div', {'class': 'info'})

            episode_title = div.find('a', {'itemprop': 'name'}).text
            episode_number = int(div.find('meta', {'itemprop': 'episodeNumber'}).attrs.get('content', '0'))

            if episode_number == 0:
                continue

            episode_score_div = div.find('span', {'class': 'ipl-rating-star__rating'})

            if not episode_score_div:
                continue

            episode_score = float(episode_score_div.text)

            if episode_score == 0:
                continue

            episode = Episode(
                index=next(index),
                season=season_number,
                number=episode_number,
                title=episode_title,
                score=episode_score,
            )

            show.add_episode(season_number, episode)

            LOGGER.info(" * Found '%s - %s'", episode.label, episode.title)

    LOGGER.info(" - Found %i episodes", next(index) - 1)

    return show
