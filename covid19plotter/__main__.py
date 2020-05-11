"""
Covid19Plotter
==============

Module for plotting trends about the novel coronavirus in various locations.
The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

import pandas as pd

from covid19plotter.mode import Mode
from covid19plotter.plotters import Plotter
from covid19plotter.plotters import USPlotter
from covid19plotter.utils import DEFAULT_INPUT_ERROR
from covid19plotter.utils import input_and_validate
from covid19plotter.utils import input_with_prompt

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_%s.csv "

GLOBAL = "global"
US = "US"

CONFIRMED = "confirmed"
DEATHS = "deaths"
RECOVERED = "recovered"

COUNTRY = "Country/Region"


class AppRunner:
    def __init__(self):
        print("Loading...")
        self.global_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, GLOBAL))
        self.global_deaths_df = pd.read_csv(BASE_URL % (DEATHS, GLOBAL))
        self.global_recoveries_df = pd.read_csv(BASE_URL % (RECOVERED, GLOBAL))
        self.us_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, US))
        self.us_deaths_df = pd.read_csv(BASE_URL % (DEATHS, US))

    def run(self):
        while True:
            mode = self._prompt_for_mode()

            # Gets the global data frame based on the mode (confirmed cases,
            # deaths, or recoveries)
            global_df = self._get_global_df(mode)

            # Prompt user for country
            country = self._prompt_for_country(global_df)

            # There is a separate data frame for the US, so get the US data
            # frame if appropriate, otherwise just use the global data frame
            df = self._get_country_df(mode, country, global_df)

            if country == US:
                plotter = USPlotter()
            else:
                plotter = Plotter()

            plotter.plot(df, mode, country)

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

        mode = input_with_prompt()

        while mode == "" or mode not in "123456":
            print(DEFAULT_INPUT_ERROR)
            mode = input_with_prompt()

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

        return input_and_validate(
            prompt=prompt, options=global_df[COUNTRY].tolist())


if __name__ == "__main__":
    plotter = AppRunner()
    plotter.run()
