from integrations import imdb, omdb


def fetch(title):
    show = omdb.search(title)
    imdb.scrap(show)

    return show
