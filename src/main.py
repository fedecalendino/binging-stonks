import logging

from integrations import fetch
from plotter import plot

logging.basicConfig(level=logging.INFO)


SHOWS = [
    "The Last Airbender",
    "Breaking Bad",
    "Better Call Saul",
    "Game of Thrones",
    "House of Cards",
    "Person of Interest",
    "The Office",
    "Dexter",
    "Scrubs",
    "Gravity Falls",
    "tt1355642",  # Fullmetal Alchemist: Brotherhood
    "Death Note",
    "Community"
]

for title in SHOWS:
    show = fetch(title)
    plot(show, save=True)
