from covid19plotter.plots import PlotBase

DATA_DESCRIPTION = "Total Cases"


class TotalPlot(PlotBase):
    def _get_title(self):
        return DATA_DESCRIPTION

    def _get_subtitle(self):
        subtitle = "Total Confirmed Cases " + str(self._data[-1])
        return subtitle + " | " + super()._get_subtitle()

    def _get_ylabel(self):
        return DATA_DESCRIPTION
