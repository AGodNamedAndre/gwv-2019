#!/usr/bin/env python3
def char_lists_from(s):
    r"""
    Transform a String linewise (by newline chars) into lists of characters.

    :param s: the input string
    :return: a list of lists of characters

    >>> char_lists_from("12\n34\n")
    [['1', '2'], ['3', '4']]
    """
    lines = s.splitlines()
    return [[c for c in l] for l in lines]


def char_lists_from_fn(fn):
    with open(fn, 'r') as file:
        return char_lists_from(file.read())
