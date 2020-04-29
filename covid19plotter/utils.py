"""
Utils
=====

Utilities used throughout the app.
"""


def list_to_lower_case(lst):
    """
    Converts the strings in the given list to lower-case.

    Args:
        lst (list): List to convert to lower-case.

    Returns:
        list
    """

    for i in range(len(lst)):
        if type(lst[i]) == str:
            lst[i] = lst[i].lower()
    return lst
