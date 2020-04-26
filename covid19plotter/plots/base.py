"""
Plot Base
=========

Base functionality common to all plots.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

DEFAULT_TITLE = "COVID-19 Data"

# First day data was collected
EARLIEST = "1/22/20"

MAX_XTICKS = 10


class PlotBase:
    """
    PlotBase class. See module documentation for more information.

    Attributes:
        _df (:class:`~pd.DataFrame`): Entire :class:`~pd.DataFrame` loaded from
            a third-party source. Not all information in this
            :class:`~pd.DataFrame` will be plotted.
        _series (:class:`~pd.Series`): :class:`~pd.Series` encompassing only
            the information that will be plotted, excluding data before the
            starting date.
    """

    def __init__(self):
        self._df = None
        self._series = None
        self._starting_day = EARLIEST

    def plot(self, df, title=DEFAULT_TITLE):
        """
        Plots the given :class:`~pd.DataFrame`.

        Args:
            df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` to plot.
            title (str): Title to display on the plot.
        """

        series = df.sum()[EARLIEST:]
        self._starting_day = self._get_starting_day(series)

        self._df = df
        self._series = self._transform_series(series)

        plt.figure(num=title)
        self._plot()

        plt.xticks(rotation=90)

        # Make tick labels smaller so they can fit
        plt.tick_params(labelsize=8)

        fig = plt.gcf()

        # Add margin below the plot so x-axis dates can fit
        fig.subplots_adjust(bottom=0.15)

        ax = fig.gca()
        ax.xaxis.set_major_locator(MaxNLocator(MAX_XTICKS))

        # Make sure y-axis only uses integers
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

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

        plt.plot(self._series)

    def _get_starting_day(self, series):
        """
        Gets the starting day to use for the plot. This is calculated by
        determining the first day 1% of the total cases today was reported.

        Args:
            series (:class:`~pd.Series`): Series containing all data values.

        Returns:
            str
        """

        return (series > series.max() * 0.01).idxmax()

    def _transform_series(self, series):
        """
        Transforms the given series of values to plot it how we want. The given
        series contains all data values, even before the starting date.

        Args:
            series (:class:`~pd.Series`): :class:`~pd.Series` to transform.

        Returns:
            :class:`~pd.Series`
        """

        return series[self._starting_day:]

    def _get_subtitle(self):
        """
        Gets the text to display below the title of the plot.

        Returns:
            str
        """

        return "Last Updated: " + self._df.columns[-1]

    def _get_ylabel(self):
        """
        Gets the y-axis label.

        Returns:
            str
        """

        return None
