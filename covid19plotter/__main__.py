"""
Covid19Plotter
==============

Module for plotting trends about the novel coronavirus in various locations.
The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

from datetime import datetime
import pandas as pd

from covid19plotter.aliases import STATE_ABBREVIATIONS
from covid19plotter.mode import Mode
from covid19plotter.plots import DailyPlot
from covid19plotter.plots import TotalPlot
from covid19plotter.utils import list_to_lower_case
from covid19plotter.utils import unique

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_%s.csv "

DATE_FORMAT = "%m/%d/%y"

GLOBAL = "global"
US = "US"

CONFIRMED = "confirmed"
DEATHS = "deaths"
RECOVERED = "recovered"

COUNTRY = "Country/Region"

# Province/state header for the US
STATE = "Province_State"

# Province/state header for non-US countries/regions
PROVINCE = "Province/State"

COUNTY = "Admin2"

CONFIRMED_DATA_DESC = "Confirmed Cases"
DEATHS_DATA_DESC = "Deaths"
RECOVERIES_DATA_DESC = "Recoveries"

OPTIONS = "options"

DEFAULT_INPUT_ERROR = "Invalid input."


class Covid19Plotter:
    """
    Covid19Plotter class. See module documentation for more information.
    """

    def __init__(self):
        print("Loading...")
        self.global_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, GLOBAL))
        self.global_deaths_df = pd.read_csv(BASE_URL % (DEATHS, GLOBAL))
        self.global_recoveries_df = pd.read_csv(BASE_URL % (RECOVERED, GLOBAL))
        self.us_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, US))
        self.us_deaths_df = pd.read_csv(BASE_URL % (DEATHS, US))

        dates = []

        for df in [self.global_confirmed_df, self.global_deaths_df,
                   self.global_recoveries_df, self.us_confirmed_df,
                   self.us_deaths_df]:

            dates.append(datetime.strptime(df.columns[-1], DATE_FORMAT))

        print("Last Updated: %s\n" % max(dates).strftime(DATE_FORMAT))

    def plot(self):
        """
        Main public method for plotting the data. The data has already been
        loaded from John Hopkins University.
        """

        while True:
            mode = self._prompt_for_mode()

            global_df = self._get_global_df(mode)

            country = self._prompt_for_country(global_df)
            state = None
            county = None

            df = self._get_country_df(mode, country, global_df)

            data_desc = self._get_data_desc(mode)

            if len(df) > 1:
                state = self._prompt_for_state(df, country)
                state_header = STATE if country == US else PROVINCE

                df = self._filter_df(df, state_header, state)

                if len(df) > 1 and state:
                    county = self._prompt_for_county(df)
                    df = self._filter_df(df, COUNTY, county)

            location = self._get_location_list(country, state, county)

            plot = TotalPlot() if Mode.is_total_mode(mode) else DailyPlot()
            plot.plot(df, data_desc, location)

    def _get_global_df(self, mode):
        """
        Gets the global :class:`~pd.DataFrame` associated with the given mode.

        Args:
            mode (int): Plotting mode.

        Returns:
            :class:`~pd.DataFrame`
        """

        if Mode.is_deaths_mode(mode):
            return self.global_deaths_df
        elif Mode.is_recoveries_mode(mode):
            return self.global_recoveries_df
        return self.global_confirmed_df

    def _get_country_df(self, mode, country, global_df):
        """
        Gets the :class:`~pd.DataFrame` for the given country.

        Args:
            mode (int): Plotting mode.
            country (str): Country to plot.
            global_df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` for the
                whole world.

        Returns:
            :class:`~pd.DataFrame`
        """

        if country == US and not Mode.is_recoveries_mode(mode):
            if Mode.is_deaths_mode(mode):
                return self.us_deaths_df
            return self.us_confirmed_df
        else:
            return global_df[global_df[COUNTRY] == country]

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

    def _get_location_list(self, country, state, county):
        """
        Gets a list of the location of the plot, from specific to general.

        Args:
            country (str): Country of the plot.
            state (str): State of the plot.
            county (str): County of the plot.

        Returns:
            lst
        """

        location_list = []

        if county:
            location_list.append(county + " County")
        if state:
            location_list.append(state)
        if country:
            location_list.append(country)

        return location_list

    def _filter_df(self, df, key, value):
        """
        Filters the given :class:`~pd.DataFrame` using the given filter key and
        value.

        Args:
            df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` to filter.
            key (str): Filter key.
            value (str): Filter value.

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
            df = df[df[key] == value]

        return df

    def _prompt_for_mode(self):
        """
        Gets the desired plotting mode from the user.

        Returns:
            int
        """

        print("What type of data do you want to view?")
        print("1 - Total confirmed")
        print("2 - New confirmed")
        print("3 - Total deaths")
        print("4 - New deaths")
        print("5 - Total recoveries")
        print("6 - New recoveries")

        mode = self._input()

        while mode == "" or mode not in "123456":
            print(DEFAULT_INPUT_ERROR)
            mode = self._input()
        
        return int(mode)

    def _prompt_for_country(self, global_df):
        """
        Gets the desired country/region from the user.

        Args:
            global_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for non-US
                countries.

        Returns:
            str
        """

        prompt = "Which country/region do you want to view? (Type OPTIONS to " \
                 "see all available options)"

        return self._input_and_validate(
            prompt=prompt, options=global_df[COUNTRY].tolist())

    def _prompt_for_state(self, country_df, country):
        """
        Gets the desired state from the user.

        Args:
            country_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for the entire
                country.
            country (str): Country selected by the user.

        Returns:
            str
        """

        if country == US:
            state_df = country_df[STATE]
        else:
            state_df = country_df[PROVINCE]

        prompt = "Which state/province do you want to view? (Just press ENTER " \
                 "to see whole country, or type OPTIONS to see all available options)"

        ignore = [""]
        if country == US:
            # Allow users to specify state by abbreviation, but do not show in
            # the "OPTIONS" output
            ignore += list(STATE_ABBREVIATIONS.keys())

        state = self._input_and_validate(prompt=prompt, options=state_df.tolist(),
                                         ignore=ignore)

        state_upper = state.upper()
        if state_upper in STATE_ABBREVIATIONS:
            state = STATE_ABBREVIATIONS[state_upper]

        return state

    def _prompt_for_county(self, state_df):
        """
        Gets the desired county from the user.

        Args:
            state_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for a single
                state.

        Returns:
            str
        """

        prompt = "Which county do you want to view? (Just press ENTER to see " \
                 "whole state)"

        return self._input_and_validate(
            prompt=prompt, options=state_df[COUNTY].tolist(), ignore=[""])
    
    def _input_and_validate(self, prompt=None, options=None, ignore=None):
        """
        Gets input from a user, using a consistent prompt, and validates it.

        Returns:
            str
        """

        i = self._input(prompt)
        i_lower = i.lower()

        options = sorted(unique(options))

        if i_lower == OPTIONS:
            for option in options:
                print(option)

        lower_options = list_to_lower_case(options)
        lower_ignore = list_to_lower_case(ignore) or []

        while i_lower not in lower_options and i_lower not in lower_ignore:
            if i_lower != OPTIONS:
                print(DEFAULT_INPUT_ERROR)

            i = self._input(prompt)
            i_lower = i.lower()

            if i_lower == OPTIONS:
                for option in options:
                    print(option)

        if i == "":
            return ""
        elif i_lower in lower_ignore:
            return i

        return options[lower_options.index(i_lower)]

    def _input(self, prompt=None):
        """
        Gets input from a user, using a consistent prompt.

        Returns:
            str
        """

        if prompt is not None:
            print(prompt)

        i = input(">>> ")

        if i == "exit" or i == "quit":
            exit()

        return i.strip()


if __name__ == "__main__":
    plotter = Covid19Plotter()
    plotter.plot()
