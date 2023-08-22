"""
Set operations
"""

import itertools
from typing import Iterable


def between(a: int, b: int) -> list:
    """
    Returns a list of integers between a and b, inclusive
    """
    return list(range(a, b + 1))


def intersection(a: Iterable, *args: list) -> set:
    """
    Returns the intersection of all iterables
    """
    return set(a).intersection(*args)


def union(*args: list) -> set:
    """
    Returns the union of all iterables
    """
    return set(itertools.chain(*args))


def product(*args: list) -> set:
    """
    Returns the cartesian product of all iterables
    """
    return set(itertools.product(*args))
