"""
Total Plot
==========

Plot for displaying the running total of values.
"""

from covid19plotter.plots import PlotBase

TOTAL = "Total"


class TotalPlot(PlotBase):
    """
    TotalPlot class. See module documentation for more information.
    """

    def _get_title(self, data_desc, location):
        location_str = ""
        if type(location) == list:
            location_str = ", ".join(location)

        return "%s %s (%s)" % (TOTAL, data_desc, location_str)

    def _get_subtitle(self, data_desc):
        subtitle = "%s: %s" % (data_desc, self._series[-1])
        return subtitle + " | " + super()._get_subtitle(data_desc)
