"""
Covid19Plotter
==============

Module for plotting trends about the novel coronavirus in various locations.
The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

import matplotlib.pyplot as plt
import pandas as pd

from covid19plotter.aliases import STATE_ABBREVIATIONS
from covid19plotter.utils import array_to_lower_case
from covid19plotter.utils import get_array_diffs

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

            location = "US"

            state = self._get_state(df)
            if state != "":
                location = state
                df = df[df[STATE] == state]

                if len(df) > 1:
                    county = self._get_county(df)
                    if county != "":
                        location = county + " County, " + state
                        df = df[df[COUNTY] == county]

            if mode == TOTAL_CONFIRMED_MODE:
                self._plot_total(df, location, "Total Confirmed")
            elif mode == NEW_CONFIRMED_MODE:
                self._plot_new(df, location, "New Confirmed")
            elif mode == TOTAL_DEATHS_MODE:
                self._plot_total(df, location, "Total Deaths")
            elif mode == NEW_DEATHS_MODE:
                self._plot_new(df, location, "New Deaths")
    
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

    def _plot_total(self, df, location, data_desc):
        """
        Plots the total number of a particular statistic to date (i.e.
        confirmed cases, deaths).

        Args:
            df (:class:`~pd.DataFrame`): `~pd.DataFrame` to plot.
            location (str): Location that the data represents, regardless of
                scope (i.e. "US" or "Michigan").
            data_desc (str): Description of the data (i.e. "Total Confirmed").
        """

        last_updated = df.columns[-1]
        df = df.sum()[STARTING_DAY:]

        self._plot(df.values.tolist(), location, last_updated, data_desc)
    
    def _plot_new(self, df, location, data_desc):
        """
        Plots the daily number of a particular statistic. (i.e. confirmed
        cases, deaths).

        Args:
            df (:class:`~pd.DataFrame`): `~pd.DataFrame` to plot.
            location (str): Location that the data represents, regardless of
                scope (i.e. "US" or "Michigan").
            data_desc (str): Description of the data (i.e. "Total Confirmed").
        """

        last_updated = df.columns[-1]
        df = df.sum()[STARTING_DAY:]
        lst = get_array_diffs(df.values.tolist())

        self._plot(lst, location, last_updated, data_desc)
    
    def _plot(self, data, location, last_updated, data_desc):
        """
        Plots the given data.

        Args:
            data (list): Data to plot.
            location (str): Location that the data represents, regardless of
                scope (i.e. "US" or "Michigan").
            last_updated (str): Date that the data was last updated.
            data_desc (str): Description of the data (i.e. "Total Confirmed").
        """

        title = "%s %s (Last Updated %s)" % (location, data_desc, last_updated)

        plt.figure(num=title)
        plt.plot(data)
        plt.xlabel("Days Since 3/1/20")
        plt.ylabel(data_desc)
        plt.suptitle(title)
        plt.title("%s: %s" % (data_desc, data[-1]), size=8)
        plt.grid()
        plt.show()

    def _get_state_confirmed_data(self, state):
        """
        Gets the confirmed cases data for the given state.

        Args:
            state (str): State to use to get the confirmed cases data.

        Returns:
            :class:`~pd.DataFrame`
        """

        df = self.confirmed_df
        return df[df[STATE] == state].sum()[STARTING_DAY:]


if __name__ == "__main__":
    plotter = Covid19Plotter()
    plotter.plot()
