import math
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

DEFAULT_TITLE = "COVID-19 Data"

# 3/1/20
STARTING_DAY = "3/1/20"

MAX_XTICKS = 10


class PlotBase:
    def __init__(self):
        self._df = None
        self._data = []
        self._starting_day_idx = 0

    def plot(self, df, title=DEFAULT_TITLE):
        self._starting_day_idx = df.columns.get_loc(STARTING_DAY)

        self._df = df
        self._data = self._get_data()

        plt.figure(num=title)
        self._plot()

        # Get the dates the for x-axis
        xticklabels = self._df.columns[self._starting_day_idx:].values.tolist()

        xtick_len = len(xticklabels)

        # Get the interval between the x-axis tick dates
        xtick_interval = math.ceil(xtick_len / MAX_XTICKS)

        # Get only the visible x-axis ticks labels
        xticklabels = xticklabels[::xtick_interval]

        # Get the visible x-axis tick positions (0 to the number of days being
        # plotted)
        xticks = range(0, xtick_len, xtick_interval)

        plt.xticks(xticks, xticklabels, rotation=90)

        # Make x-axis dates smaller so they can fit
        plt.tick_params(axis="x", labelsize=8)

        fig = plt.gcf()

        # Add margin below the plot so x-axis dates can fit
        fig.subplots_adjust(bottom=0.2)

        # Make sure y-axis only uses integers
        fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.xlabel(self._get_xlabel())
        plt.ylabel(self._get_ylabel())
        plt.suptitle(title)
        plt.title(self._get_subtitle(), size=8)
        plt.grid()
        plt.show()

    def _plot(self):
        """
        Internal method responsible for actually plotting the line(s) on the
        plot.
        """

        plt.plot(self._data)

    def _get_data(self):
        return self._df.sum()[self._starting_day_idx:].values.tolist()

    def _get_subtitle(self):
        return "Last Updated: " + self._df.columns[-1]

    def _get_xlabel(self):
        return "Days Since 3/1/20"

    def _get_ylabel(self):
        return None
