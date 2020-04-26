import matplotlib.pyplot as plt

DEFAULT_TITLE = "COVID-19 Data"

# 3/1/20
STARTING_DAY = 50


class PlotBase:
    def __init__(self):
        self._df = None
        self._data = []

    def plot(self, df, title=DEFAULT_TITLE):
        self._df = df
        self._data = self._get_data()

        plt.figure(num=title)
        plt.plot(self._data)
        plt.xlabel(self._get_xlabel())
        plt.ylabel(self._get_ylabel())
        plt.suptitle(title)
        plt.title(self._get_subtitle(), size=8)
        plt.grid()
        plt.show()

    def _get_data(self):
        print(self._df.sum()[STARTING_DAY:])
        return self._df.sum()[STARTING_DAY:].values.tolist()

    def _get_subtitle(self):
        return "Last Updated: " + self._df.columns[-1]

    def _get_xlabel(self):
        return "Days Since 3/1/20"

    def _get_ylabel(self):
        return None
