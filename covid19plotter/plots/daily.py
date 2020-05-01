"""
Daily Plot
==========

Plot for displaying daily increases in values.
"""

import pandas as pd
import matplotlib.pyplot as plt

from covid19plotter.plots import PlotBase

DAILY = "Daily"

ONE_WEEK = 7

MOVING_AVG_COLOR = (0.12, 0.47, 0.71, 0.5)
MOVING_AVG_STYLE = "--"


class DailyPlot(PlotBase):
    """
    DailyPlot class. See module documentation for more information.
    """

    def _plot(self):
        super()._plot()

        series = pd.Series(self._series)
        moving_average = series.rolling(ONE_WEEK).mean().values.tolist()

        # Move moving average line back a few days so it follows the trend of
        # the main line
        moving_average = moving_average[round((ONE_WEEK-1)/2):]

        plt.plot(moving_average, color=MOVING_AVG_COLOR,
                 linestyle=MOVING_AVG_STYLE)

    def _get_starting_day(self, series):
        daily_values = self._get_daily_values(series)
        return (daily_values > daily_values.max() * 0.01).idxmax()

    def _transform_series(self, series):
        transformed_series = self._get_daily_values(series)
        return super()._transform_series(transformed_series)

    def _get_title(self, data_desc, location):
        location_str = ""
        if type(location) == list:
            location_str = ", ".join(location)

        return "%s %s (%s)" % (DAILY, data_desc, location_str)

    def _get_subtitle(self, data_desc):
        last_updated = self._df.columns[-1]
        return data_desc + " on %s: %s" % (last_updated, self._series[-1])

    def _get_daily_values(self, series):
        """
        Returns the increase in value at each index in the given
        :class:`~pd.Series`.

        Args:
            series (:class:`~pd.Series`): :class:`~pd.Series` to use to
                calculate the increase in values.

        Returns:
            :class:`~pd.Series`
        """

        return series - series.shift(1)
