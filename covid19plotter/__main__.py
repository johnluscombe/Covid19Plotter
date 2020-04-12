import matplotlib.pyplot as plt
import pandas as pd

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


def array_to_lower_case(arr):
    for i in range(len(arr)):
        arr[i] = arr[i].lower()
    return arr


def get_array_diffs(arr):
    if len(arr) > 0:
        diffs = arr[:1]
        for i in range(1, len(arr)):
            diffs.append(arr[i] - arr[i - 1])
        return diffs
    return []


class Covid19Plotter:
    def __init__(self):
        print("Loading...")
        self.confirmed_df = pd.read_csv(BASE_URL % "confirmed")
        self.deaths_df = pd.read_csv(BASE_URL % "deaths")

    def plot(self):
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
        print("Which state do you want to view? (Just press ENTER to see whole country)")

        state = self._input()
        states = array_to_lower_case(country_df[STATE].tolist())

        while state != "" and state.lower() not in states:
            print("Invalid state.")
            state = self._input()

        return state

    def _get_county(self, state_df):
        print("Which county do you want to view? (Just press ENTER to see whole state)")

        county = self._input()
        counties = array_to_lower_case(state_df[COUNTY].tolist())

        while county != "" and county.lower() not in counties:
            print("Invalid county.")
            county = self._input()

        return county
    
    def _input(self):
        i = input(">>> ")
        if i == "exit" or i == "quit":
            exit()
        return i
    
    def _plot_total(self, df, location, data_desc):
        last_updated = df.columns[-1]
        df = df.sum()[STARTING_DAY:]

        self._plot(df.values.tolist(), location, last_updated, data_desc)
    
    def _plot_new(self, df, location, data_desc):
        last_updated = df.columns[-1]
        df = df.sum()[STARTING_DAY:]
        lst = get_array_diffs(df.values.tolist())

        self._plot(lst, location, last_updated, data_desc)
    
    def _plot(self, data, location, last_updated, data_desc):
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
        df = self.confirmed_df
        return df[df[STATE] == state].sum()[STARTING_DAY:]


if __name__ == "__main__":
    plotter = Covid19Plotter()
    plotter.plot()
