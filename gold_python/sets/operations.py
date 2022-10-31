import itertools
from typing import Iterable

def between(a: int, b: int) -> list:
    return list(range(a, b+1))

def intersection(a: Iterable, *args: list) -> set:
    return set(a).intersection(*args)

def union(*args: list) -> set:
    return set(itertools.chain(*args))

def product(*args: list) -> set:
    return set(itertools.product(*args))
