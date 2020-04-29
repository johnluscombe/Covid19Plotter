"""
Enums
=====

All enums used by the app.
"""


class Mode:
    """
    Mode enum, encapsulating all the different plotting modes that the user can
    specify.
    """

    TOTAL_CONFIRMED = 1
    NEW_CONFIRMED = 2
    TOTAL_DEATHS = 3
    NEW_DEATHS = 4
    TOTAL_RECOVERIES = 5
    NEW_RECOVERIES = 6

    @staticmethod
    def is_confirmed_mode(mode):
        """
        Returns whether the mode specified by the user is total confirmed or
        new confirmed.

        Args:
            mode (int): Mode specified by the user.

        Returns:
            bool
        """

        return mode in [Mode.TOTAL_CONFIRMED, Mode.NEW_CONFIRMED]

    @staticmethod
    def is_deaths_mode(mode):
        """
        Returns whether the mode specified by the user is total deaths or new
        deaths.

        Args:
            mode (int): Mode specified by the user.

        Returns:
            bool
        """

        return mode in [Mode.TOTAL_DEATHS, Mode.NEW_DEATHS]

    @staticmethod
    def is_recoveries_mode(mode):
        """
        Returns whether the mode specified by the user is total recoveries or
        new recoveries.

        Args:
            mode (int): Mode specified by the user.

        Returns:
            bool
        """

        return mode in [Mode.TOTAL_RECOVERIES, Mode.NEW_RECOVERIES]

    @staticmethod
    def is_total_mode(mode):
        """
        Returns whether the mode specified by the user is total confirmed,
        total deaths, and total recoveries.

        Args:
            mode (int): Mode specified by the user.

        Returns:
            bool
        """

        return mode in [Mode.TOTAL_CONFIRMED, Mode.TOTAL_DEATHS,
                        Mode.TOTAL_RECOVERIES]

    @staticmethod
    def is_new_mode(mode):
        """
        Returns whether the mode specified by the user is new confirmed, new
        deaths, and new recoveries.

        Args:
            mode (int): Mode specified by the user.

        Returns:
            bool
        """

        return mode in [Mode.NEW_CONFIRMED, Mode.NEW_DEATHS,
                        Mode.NEW_RECOVERIES]
