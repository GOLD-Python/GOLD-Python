from typing import Any, Callable, Iterable


def combine(functions, *args):
    """
    Combines the results of multiple delta functions and returns every state that returns a different state. This is used on the deltafunc decorator for Non-Deterministic Finite Automata
    """
    nextStates = []
    for func in functions:
        state = func(*args)
        if state != None:
            nextStates.append(state)
    return nextStates

def combine_stack(functions, *args):
    """
    Combines the results of multiple delta functions and the state of the stacks within the calls and returns every new state as well as stack result. This is used on the pushdownfunc decorator for Pushdown Automata
    """
    nextStates = []
    mutableArgs = list(args)
    stack = mutableArgs[-2]
    for func in functions:
        mutableArgs[-2] = stack.__copy__()
        state = func(*mutableArgs)
        if state != None:
            nextStates.append((state, mutableArgs[-2]))
    return nextStates


def call_func_iterable(func: Callable, args: Iterable | Any, *constants: tuple):
    """
    Calls the function by splitting the args into different calls depending if the args
    paremeter is an iterable or not. All other arguments are supplied to the right of the
    function in the same order
    """
    if hasattr(args, '__iter__') and not isinstance(args, str):
        return func(*args, *constants)
    else:
        return func(args, *constants)
