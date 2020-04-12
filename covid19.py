import matplotlib.pyplot as plt
import pandas as pd

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_%s_US.csv"

CONFIRMED_DF = pd.read_csv(BASE_URL % "confirmed")
DEATHS_DF = pd.read_csv(BASE_URL % "deaths")

TOTAL_CONFIRMED_MODE = 1
NEW_CONFIRMED_MODE = 2
TOTAL_DEATHS_MODE = 3
NEW_DEATHS_MODE = 4

# 3/1/20
STARTING_DAY = 43

LAST_UPDATED = CONFIRMED_DF.columns[-1]

TOTAL_CASES = "Total Cases"
NEW_CASES = "New Cases"

STATE = "Province_State"
COUNTY = "Admin2"


class Covid19Plotter:
    def plot(self):
        while True:
            mode = self._get_mode()
            state = self._get_state(mode)

            if state != "":
                confirmed_df = CONFIRMED_DF[CONFIRMED_DF[STATE] == state]
                deaths_df = DEATHS_DF[DEATHS_DF[STATE] == state]

                if mode == TOTAL_CONFIRMED_MODE:
                    self._plot_total(confirmed_df, state, "Total Confirmed")
                elif mode == NEW_CONFIRMED_MODE:
                    self._plot_new(confirmed_df, state, "New Confirmed")
                elif mode == TOTAL_DEATHS_MODE:
                    self._plot_total(deaths_df, state, "Total Deaths")
                elif mode == NEW_DEATHS_MODE:
                    self._plot_new(deaths_df, state, "New Deaths")
            else:
                if mode == TOTAL_CONFIRMED_MODE:
                    self._plot_total(CONFIRMED_DF, "US", "Total Confirmed")
                elif mode == NEW_CONFIRMED_MODE:
                    self._plot_new(CONFIRMED_DF, "US", "New Confirmed")
                elif mode == TOTAL_DEATHS_MODE:
                    self._plot_total(DEATHS_DF, "US", "Total Deaths")
                elif mode == NEW_DEATHS_MODE:
                    self._plot_new(DEATHS_DF, "US", "New Deaths")
    
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
    
    def _get_state(self, mode):
        print("What state do you want to view? (Just press ENTER to see whole country)")

        if mode == TOTAL_DEATHS_MODE or mode == NEW_DEATHS_MODE:
            df = DEATHS_DF
        else:
            df = CONFIRMED_DF

        state = self._input()
        states = self._array_to_lower_case(df[STATE].tolist())

        while state != "" and state.lower() not in states:
            print("Invalid state.")
            state = self._input()

        return state

    def _array_to_lower_case(self, arr):
        for i in range(len(arr)):
            arr[i] = arr[i].lower()
        return arr
    
    def _input(self):
        i = input(">>> ")
        if i == "exit" or i == "quit":
            exit()
        return i
    
    def _plot_total(self, df, location, data_desc):
        lst = df.sum()[STARTING_DAY:].values.tolist()
        self._plot(lst, location, data_desc)
    
    def _plot_new(self, df, location, data_desc):
        lst = df.sum()[STARTING_DAY:].values.tolist()
        self._plot(self._get_diffs(lst), location, data_desc)
    
    def _plot(self, conf_list, location, data_desc):
        title = "%s %s (Last Updated %s)" % (location, data_desc, LAST_UPDATED)

        plt.figure(num=title)
        plt.plot(conf_list)
        plt.xlabel("Days Since 3/1/20")
        plt.ylabel(data_desc)
        plt.suptitle(title)
        plt.title("%s: %s" % (data_desc, conf_list[-1]), size=8)
        plt.grid()
        plt.show()

    def _get_state_confirmed_data(self, state):
        return CONFIRMED_DF[CONFIRMED_DF[STATE] == state].sum()[STARTING_DAY:]
    
    def _get_diffs(self, arr):
        if len(arr) > 0:
            diffs = arr[:1]
            for i in range(1, len(arr)):
                diffs.append(arr[i] - arr[i-1])
            return diffs
        return []


plotter = Covid19Plotter()
plotter.plot()
