"""
This module contains functions for set operations

The functions in this module can be used to perform set operations on iterables before
feeding them to the automata classes in the automata module. This simplifies the process
of creating automata, since the user does not have to worry about the format of the
iterables.
"""

import itertools
from typing import Iterable, List, Set


def between(a: int, b: int) -> List[int]:
    """
    Returns a list of integers between a and b, inclusive
    """
    return list(range(a, b + 1))


def between_char(a: str, b: str) -> List[str]:
    """
    Returns a list of characters between a and b, inclusive
    """
    return [chr(i) for i in range(ord(a), ord(b) + 1)]


def intersection(a: Iterable, *args: List) -> Set:
    """
    Returns the intersection of all iterables
    """
    return set(a).intersection(*args)


def union(*args: List) -> Set:
    """
    Returns the union of all iterables
    """
    return set(itertools.chain(*args))


def product(*args: List) -> Set:
    """
    Returns the cartesian product of all iterables
    """
    return set(itertools.product(*args))
