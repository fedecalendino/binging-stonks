import logging

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

from plotter.settings import (
    AUTO_SCALE,
    BACKGROUND,
    COLORS,
    FOREGROUND,
    LABEL_SIZE,
    MIDDLEGROUND,
    OUTPUT_PATH,
    TITLE_SIZE,
)
from classes import Show

LOGGER = logging.getLogger("plotter")


def _setup(show: Show):
    fig = plt.figure(
        figsize=(10 + 5 * max(show.episode_count / 25, 1), 7.5),
        dpi=80,
        facecolor=BACKGROUND
    )

    ax = plt.axes(facecolor=BACKGROUND)
    ax.set_prop_cycle(color=COLORS)

    if not AUTO_SCALE:
        ax.set_ylim(1, 10)
        ax.autoscale(False, axis='y')

    # Title
    plt.title(str(show), fontsize=TITLE_SIZE)

    # Labels
    x_label = f"{show.episode_count} episodes"

    if show.season_count > 1:
        x_label = f"{x_label} - {show.season_count} seasons"

    plt.xlabel(x_label, fontsize=LABEL_SIZE)
    plt.ylabel("episode score", fontsize=LABEL_SIZE)

    return fig, ax


def plot(show: Show, save: bool = False):
    LOGGER.info("Plotting episodes of %s", show.title)

    fig, ax = _setup(show)

    xlabels = []
    gx, gy = [], []

    for season, episodes in show.seasons.items():
        if not episodes:
            continue

        x = list(map(lambda e: e.index, episodes))
        y = list(map(lambda e: e.score, episodes))

        xlabels.extend(map(lambda e: e.label, episodes))

        gx.extend(x)
        gy.extend(y)

        z = np.polyfit(x, y, deg=1)
        p = np.poly1d(z)

        sp_x = np.linspace(episodes[0].index, episodes[-1].index, len(episodes) * 10)
        sp_y = interpolate.make_interp_spline(x, y)(sp_x)

        plt.plot(sp_x, sp_y)

        plt.scatter(x, y)
        plt.plot(x, p(x), color=MIDDLEGROUND)

    gz = np.polyfit(gx, gy, deg=1)
    gp = np.poly1d(gz)

    plt.plot(gx, gp(gx), color=FOREGROUND)

    # Ticks
    plt.xticks(range(1, len(xlabels) + 1), rotation=90)
    ax.set_xticklabels(xlabels)

    if save:
        path = OUTPUT_PATH / f"{show.slug}.png"
        plt.savefig(path)
        LOGGER.info(" - Saved plot into %s", path)

    return plt
