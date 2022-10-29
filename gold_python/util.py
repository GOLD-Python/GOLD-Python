"""
Combines the results of multiple delta functions and returns every state that returns a different state. This is used on the deltafunc decorator for Non-Deterministic Finite Automata
"""
def combine(functions, *args):
    nextStates = []
    for func in functions:
        state = func(*args)
        if state != None:
            nextStates.append(state)
    return nextStates

"""
Combines the results of multiple delta functions and the state of the stacks within the calls and returns every new state as well as stack result. This is used on the pushdownfunc decorator for Pushdown Automata
"""
def combine_stack(functions, *args):
    nextStates = []
    mutableArgs = list(args)
    stack = mutableArgs[-2]
    for func in functions:
        mutableArgs[-2] = stack.__copy__()
        state = func(*mutableArgs)
        if state != None:
            nextStates.append((state, mutableArgs[-2]))
    return nextStates
