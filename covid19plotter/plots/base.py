import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

DEFAULT_TITLE = "COVID-19 Data"

# First day data was collected
EARLIEST = "1/22/20"

STARTING_DAY = "3/1/20"

MAX_XTICKS = 10


class PlotBase:
    def __init__(self):
        self._df = None
        self._series = None

    def plot(self, df, title=DEFAULT_TITLE):
        self._df = df
        self._series = self._transform_series(df.sum()[EARLIEST:])

        plt.figure(num=title)
        self._plot()

        plt.xticks(rotation=90)

        # Make x-axis dates smaller so they can fit
        plt.tick_params(axis="x", labelsize=8)

        fig = plt.gcf()

        # Add margin below the plot so x-axis dates can fit
        fig.subplots_adjust(bottom=0.2)

        ax = fig.gca()
        ax.xaxis.set_major_locator(MaxNLocator(MAX_XTICKS))

        # Make sure y-axis only uses integers
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

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

        plt.plot(self._series)

    def _transform_series(self, series):
        return series[STARTING_DAY:]

    def _get_subtitle(self):
        return "Last Updated: " + self._df.columns[-1]

    def _get_xlabel(self):
        return "Days Since 3/1/20"

    def _get_ylabel(self):
        return None
