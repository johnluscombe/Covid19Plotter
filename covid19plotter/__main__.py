"""
Covid19Plotter
==============

Module for plotting trends about the novel coronavirus in various locations.
The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

import pandas as pd

from covid19plotter.aliases import STATE_ABBREVIATIONS
from covid19plotter.plots import DailyPlot
from covid19plotter.plots import TotalPlot
from covid19plotter.utils import array_to_lower_case

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_US.csv "

TOTAL_CONFIRMED_MODE = 1
NEW_CONFIRMED_MODE = 2
TOTAL_DEATHS_MODE = 3
NEW_DEATHS_MODE = 4

# 3/1/20
STARTING_DAY = 43

TOTAL_CASES = "Total Cases"
NEW_CASES = "New Cases"

STATE = "Province_State"
COUNTY = "Admin2"


class Covid19Plotter:
    """
    Covid19Plotter class. See module documentation for more information.
    """

    def __init__(self):
        print("Loading...")
        self.confirmed_df = pd.read_csv(BASE_URL % "confirmed")
        self.deaths_df = pd.read_csv(BASE_URL % "deaths")

    def plot(self):
        """
        Main public method for plotting the data. The data has already been
        loaded from John Hopkins University.
        """

        while True:
            mode = self._get_mode()

            if mode == TOTAL_DEATHS_MODE or mode == NEW_DEATHS_MODE:
                df = self.deaths_df
            else:
                df = self.confirmed_df

            state = self._get_state(df)
            if state != "":
                df = df[df[STATE] == state]

                if len(df) > 1:
                    county = self._get_county(df)
                    if county != "":
                        df = df[df[COUNTY] == county]

            if mode == TOTAL_CONFIRMED_MODE:
                plot = TotalPlot()
                plot.plot(df, title="Total Confirmed Cases")
            elif mode == NEW_CONFIRMED_MODE:
                plot = DailyPlot()
                plot.plot(df, title="Daily Confirmed Cases")
            elif mode == TOTAL_DEATHS_MODE:
                plot = TotalPlot()
                plot.plot(df, title="Total Deaths")
            elif mode == NEW_DEATHS_MODE:
                plot = DailyPlot()
                plot.plot(df, title="Daily Deaths")
    
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

        mode = self._input()

        while mode not in "1234":
            if mode != "":
                print("Invalid input.")
            mode = self._input()
        
        return int(mode)
    
    def _get_state(self, country_df):
        """
        Gets the desired state from the user.

        Args:
            country_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for the entire
                country.

        Returns:
            str
        """

        print("Which state do you want to view? (Just press ENTER to see whole country)")

        state = self._input()
        states = array_to_lower_case(country_df[STATE].tolist())

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
        counties = array_to_lower_case(state_df[COUNTY].tolist())

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
