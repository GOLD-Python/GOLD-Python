import itertools


def between(a: int, b: int) -> list:
    return list(range(a, b+1))

def product(*args: list) -> set:
    return set(itertools.product(*args))
