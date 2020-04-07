from slugify import slugify


class Episode:

    def __init__(self, index, season, number, title, score):
        self.index = index
        self.season = season
        self.number = number
        self.title = title
        self.score = score

    @property
    def label(self):
        return f"{self.season:02d}x{self.number:02d}"

    def __str__(self):
        return f"{self.label}: {self.title}"


class Show:
    def __init__(self, imdb_id: str, title: str, seasons: int):
        self.imdb_id = imdb_id
        self.title = title
        self.slug = slugify(title)

        self.plot = None
        self.year = None
        self.poster = None
        self.rating = None
        self.votes = None

        self.seasons = {season: [] for season in range(1, seasons + 1)}

    @property
    def season_count(self):
        return len(self.seasons)

    @property
    def episode_count(self):
        return sum(map(len, self.seasons.values()))

    def add_episode(self, season: int, episode: Episode):
        self.seasons[season].append(episode)

    @property
    def url(self):
        return f"https://www.imdb.com/title/{self.imdb_id}"

    def __str__(self):
        return f"({self.year}) {self.title} - {self.rating}"
