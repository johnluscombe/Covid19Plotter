from covid19plotter.aliases import STATE_ABBREVIATIONS
from covid19plotter.mode import Mode
from covid19plotter.plots import DailyPlot
from covid19plotter.plots import TotalPlot
from covid19plotter.plotters import Plotter
from covid19plotter.regions import REGIONS
from covid19plotter.utils import input_and_validate

STATE = "Province_State"
COUNTY = "Admin2"


class USPlotter(Plotter):
    """
    :class:`~Covid19Plotter` for the US.
    """

    def plot(self, df, mode, country):
        """
        Plots the given data frame.

        Args:
            df (:class:`~DataFrame`): Data frame to plot.
            mode (int): Plotting mode.
            country (str): Country specified by the user.
        """

        state, region, county = None, None, None

        # If there is more than one state/province available, prompt the
        # user for the state
        if len(df) > 1:
            state = self._prompt_for_state(df)

        df = self._filter_df(df, STATE, state)

        regions_supported = state in REGIONS

        # Ask for region for US state
        if len(df) > 1 and regions_supported:
            state_regions = list(REGIONS[state].keys())
            region = self._prompt_for_region(state_regions)

        # If region is specified, filter data frame by counties for that
        # region
        if region:
            df = self._filter_df(df, COUNTY, REGIONS[state][region])

        if len(df) > 1 and state and (not regions_supported or region):
            county = self._prompt_for_county(df)
            df = self._filter_df(df, COUNTY, county)

        location = self._get_location_list(country, state, region, county)

        plot = TotalPlot() if Mode.is_total_mode(mode) else DailyPlot()
        plot.plot(df, self._get_data_desc(mode), location)

    def _get_location_list(self, country, state=None, region=None, county=None):
        """
        Gets a list of the location of the plot, from specific to general.

        Args:
            country (str): Country of the plot.
            state (str): State of the plot.
            region (str): Region of the plot.
            county (str): County of the plot.

        Returns:
            lst
        """

        location_list = []

        if county:
            location_list.append(county + " County")
        elif region:
            location_list.append(region + " Region")

        if state:
            location_list.append(state)
        if country:
            location_list.append(country)

        return location_list

    def _prompt_for_state(self, country_df):
        """
        Gets the desired state from the user.

        Args:
            country_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for the entire
                country.

        Returns:
            str
        """

        prompt = self._get_state_prompt()
        state_df = country_df[STATE]
        ignore = list(STATE_ABBREVIATIONS.keys()) + [""]

        state = input_and_validate(prompt=prompt, options=state_df.tolist(),
                                   ignore=ignore)

        state_upper = state.upper()
        if state_upper in STATE_ABBREVIATIONS:
            state = STATE_ABBREVIATIONS[state_upper]

        return state

    def _prompt_for_region(self, valid_regions):
        """
        Gets the desired region from the user.

        Args:
            valid_regions (list): List of valid regions.

        Returns:
            str
        """

        prompt = "Which region do you want to view? (Just press ENTER to see " \
                 "all regions, or type OPTIONS to see all available options)"

        return input_and_validate(prompt=prompt, options=valid_regions,
                                        ignore=[""])

    def _prompt_for_county(self, region_df):
        """
        Gets the desired county from the user.

        Args:
            region_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for a single
                region (or state if region is not applicable).

        Returns:
            str
        """

        prompt = "Which county do you want to view? (Just press ENTER to see " \
                 "all counties, or type OPTIONS to see all available options)"

        return input_and_validate(
            prompt=prompt, options=region_df[COUNTY].tolist(), ignore=[""])
