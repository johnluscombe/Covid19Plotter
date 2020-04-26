from covid19plotter.plots import PlotBase

DATA_DESCRIPTION = "Daily Cases"


def get_array_diffs(arr):
    if len(arr) > 0:
        diffs = arr[:1]
        for i in range(1, len(arr)):
            diffs.append(arr[i] - arr[i - 1])
        return diffs
    return []


class DailyPlot(PlotBase):
    def _get_data(self):
        return get_array_diffs(super()._get_data())

    def _get_title(self):
        return DATA_DESCRIPTION

    def _get_subtitle(self):
        last_updated = self._df.columns[-1]
        return "Confirmed Cases on %s: %s" % (last_updated, self._data[-1])

    def _get_ylabel(self):
        return DATA_DESCRIPTION
