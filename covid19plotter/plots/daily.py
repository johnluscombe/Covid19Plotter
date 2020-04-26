import pandas as pd
import matplotlib.pyplot as plt

from covid19plotter.plots import PlotBase

DATA_DESCRIPTION = "Daily Cases"

ONE_WEEK = 7

MOVING_AVG_COLOR = (0.12, 0.47, 0.71, 0.5)
MOVING_AVG_STYLE = "--"


class DailyPlot(PlotBase):
    def _plot(self):
        super()._plot()

        series = pd.Series(self._series)
        moving_average = series.rolling(ONE_WEEK).mean().values.tolist()

        # Move moving average line back a few days so it follows the trend of
        # the main line
        moving_average = moving_average[round((ONE_WEEK-1)/2):]

        plt.plot(moving_average, color=MOVING_AVG_COLOR,
                 linestyle=MOVING_AVG_STYLE)

    def _transform_series(self, series):
        transformed_series = series - series.shift(1)
        return super()._transform_series(transformed_series)

    def _get_title(self):
        return DATA_DESCRIPTION

    def _get_subtitle(self):
        last_updated = self._df.columns[-1]
        return "Confirmed Cases on %s: %s" % (last_updated, self._series[-1])

    def _get_ylabel(self):
        return DATA_DESCRIPTION
