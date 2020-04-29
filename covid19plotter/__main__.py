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

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_%s.csv "

DATE_FORMAT = "%m/%d/%y"

GLOBAL = "global"
US = "US"

CONFIRMED = "confirmed"
DEATHS = "deaths"
RECOVERED = "recovered"

TOTAL_CASES = "Total Cases"
NEW_CASES = "New Cases"

COUNTRY = "Country/Region"

# Province/state header for the US
STATE = "Province_State"

# Province/state header for non-US countries/regions
PROVINCE = "Province/State"

COUNTY = "Admin2"


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
            mode = self._get_mode()

            if Mode.is_deaths_mode(mode):
                df = self.global_deaths_df
                data_desc = "Deaths"
            elif Mode.is_recoveries_mode(mode):
                df = self.global_recoveries_df
                data_desc = "Recoveries"
            else:
                df = self.global_confirmed_df
                data_desc = "Confirmed Cases"

            country = self._get_country(df)
            if country == US and not Mode.is_recoveries_mode(mode):
                if Mode.is_deaths_mode(mode):
                    df = self.us_deaths_df
                else:
                    df = self.us_confirmed_df
            else:
                df = df[df[COUNTRY] == country]

            if len(df) > 1:
                state = self._get_state(df, country)

                if country == US:
                    state_header = STATE
                else:
                    state_header = PROVINCE

                if state == "":
                    state_nan_df = df[state_header].isna()

                    if state_nan_df.sum() == 1:
                        # If a row exists in the country data frame where the
                        # state is NaN, it is the total row, so use that for
                        # the data
                        df = df[state_nan_df]
                else:
                    df = df[df[state_header] == state]

                    if len(df) > 1:
                        county = self._get_county(df)
                        if county == "":
                            county_nan_df = df[COUNTY].isna()

                            if county_nan_df.sum() == 1:
                                # If a row exists in the state data frame where
                                # the country is NaN, it is the total row, so
                                # use that for the data
                                df = df[county_nan_df]
                        else:
                            df = df[df[COUNTY] == county]

            if Mode.is_total_mode(mode):
                plot = TotalPlot()
            else:
                plot = DailyPlot()

            plot.plot(df, data_desc)

    def _get_mode(self):
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

        while mode not in "123456":
            if mode != "":
                print("Invalid input.")
            mode = self._input()
        
        return int(mode)

    def _get_country(self, global_df):
        """
        Gets the desired country/region from the user.

        Args:
            global_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for non-US
                countries.

        Returns:
            str
        """

        print("Which country/region do you want to view?")

        country = self._input()
        countries = list_to_lower_case(global_df[COUNTRY].tolist())

        while country.lower() not in countries:
            print("Invalid country.")
            country = self._input()

        return country
    
    def _get_state(self, country_df, country):
        """
        Gets the desired state from the user.

        Args:
            country_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for the entire
                country.
            country (str): Country selected by the user.

        Returns:
            str
        """

        print("Which state/province do you want to view? (Just press ENTER to see whole country)")

        state = self._input()

        if country == US:
            state_df = country_df[STATE]
        else:
            state_df = country_df[PROVINCE]

        states = list_to_lower_case(state_df.tolist())

        if state in STATE_ABBREVIATIONS:
            state = STATE_ABBREVIATIONS[state]

        while state != "" and state.lower() not in states:
            print("Invalid state.")
            state = self._input()

            if state in STATE_ABBREVIATIONS:
                state = STATE_ABBREVIATIONS[state]

        return state

    def _get_county(self, state_df):
        """
        Gets the desired county from the user.

        Args:
            state_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for a single
                state.

        Returns:
            str
        """

        print("Which county do you want to view? (Just press ENTER to see whole state)")

        county = self._input()
        counties = list_to_lower_case(state_df[COUNTY].tolist())

        while county != "" and county.lower() not in counties:
            print("Invalid county.")
            county = self._input()

        return county
    
    def _input(self):
        """
        Gets input from a user, using a consistent prompt.

        Returns:
            str
        """

        i = input(">>> ")
        if i == "exit" or i == "quit":
            exit()
        return i


if __name__ == "__main__":
    plotter = Covid19Plotter()
    plotter.plot()
