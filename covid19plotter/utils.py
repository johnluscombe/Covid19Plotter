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

    if lst is None:
        return None

    new_lst = []

    for i in range(len(lst)):
        if type(lst[i]) == str:
            new_lst.append(lst[i].lower())

    return new_lst


def unique(lst):
    """
    Returns the unique items in the given list.

    Args:
        lst (lst): List to get the unique items from.

    Returns:
        list
    """

    return list(dict.fromkeys(lst))
