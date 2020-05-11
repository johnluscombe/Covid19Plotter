from covid19plotter.mode import Mode
from covid19plotter.plots import DailyPlot
from covid19plotter.plots import TotalPlot
from covid19plotter.utils import input_and_validate

STATE = "Province/State"

CONFIRMED_DATA_DESC = "Confirmed Cases"
DEATHS_DATA_DESC = "Deaths"
RECOVERIES_DATA_DESC = "Recoveries"


class Plotter:
    """
    COVID-19 plotters functionality for all countries.
    """

    def plot(self, df, mode, country):
        """
        Plots the given data frame.

        Args:
            df (:class:`~DataFrame`): Data frame to plot.
            mode (int): Plotting mode.
            country (str): Country specified by the user.
        """

        state = None

        if len(df) > 1:
            state = self._prompt_for_state(df)

        df = self._filter_df(df, STATE, state)

        data_desc = self._get_data_desc(mode)
        location = self._get_location_list(country, state)

        plot = TotalPlot() if Mode.is_total_mode(mode) else DailyPlot()
        plot.plot(df, data_desc, location)

    def _get_data_desc(self, mode):
        """
        Gets the description of the data, using the given mode.

        Args:
            mode (int): Plotting mode.

        Returns:
            str
        """

        if Mode.is_deaths_mode(mode):
            return DEATHS_DATA_DESC
        elif Mode.is_recoveries_mode(mode):
            return RECOVERIES_DATA_DESC
        return CONFIRMED_DATA_DESC

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

        return input_and_validate(prompt=prompt, options=state_df.tolist(),
                                  ignore=[""])

    def _get_state_prompt(self):
        """
        Returns the prompt to use to ask the user for the state.

        Returns:
            str
        """

        return "Which state/province do you want to view? (Just press ENTER " \
               "to see all states, or type OPTIONS to see all available options)"

    def _get_location_list(self, country, state=None, **kwargs):
        """
        Gets a list of the location of the plot, from specific to general.

        Args:
            country (str): Country of the plot.
            state (str): State of the plot.

        Returns:
            lst
        """

        location_list = []

        if state:
            location_list.append(state)
        if country:
            location_list.append(country)

        return location_list

    def _filter_df(self, df, key, value):
        """
        Filters the given :class:`~pd.DataFrame` using the given filter key and
        values.

        Args:
            df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` to filter.
            key (str): Filter key.
            values (str or list): Filter values.

        Returns:
            :class:`~pd.DataFrame`
        """

        if not value:
            nan_df = df[key].isna()

            if nan_df.sum() == 1:
                # If a row exists in the filtered data frame where the value of
                # the given key is NaN, it is the total row, so use that for
                # the data
                df = df[nan_df]
        else:
            if type(value) != list:
                value = [value]

            df = df[df[key].isin(value)]

        return df
