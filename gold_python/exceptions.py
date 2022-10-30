
class SymbolNotFoundException(Exception):
    """
    Raised when a symbol is used when it's not part of the alphabet
    """

    def __init__(self, symbol) -> None:
        super().__init__(f"Could not find symbol {symbol} on the alphabet of the automata")

class FunctionDefinitionNotFoundException(Exception):
    """
    Raised when the definition of a function could not be found for the length of parameters given
    """

    def __init__(self, name, num) -> None:
        super().__init__(f"Could not find a definition for the function {name} with {num} parameters")

class PathNotFoundException(Exception):
    """
    Raised when no path was found on a deterministic automata
    """

    def __init__(self, symbol, state) -> None:
        super().__init__(f"No path was found for the symbol {symbol} from the state {state}")

class MultiplePathsFoundException(Exception):
    """
    Raised when multiple paths are found on a deterministic automata
    """

    def __init__(self, symbol, state) -> None:
        super().__init__(f"Multiple paths have been found for the symbol {symbol} from the state {state}, when only one path should be taken")

class StateNotFoundException(Exception):
    """
    Raised when the state is not found on the set of possible states for the automata
    """

    def __init__(self, symbol, state, errstate) -> None:
        super().__init__(f"The state {errstate} generated from the state {state} and symbol {symbol} is not part of the set of possible states for the automata")

class NotEnoughArgumentsException(Exception):
    """
    Raised when not enough arguments have been supplied to the delta-like function
    """

    def __init__(self, name) -> None:
        super().__init__(f"Not enough arguments have been supplied to the delta-like function {name}")

class OutputSymbolNotFoundException(Exception):
    """
    Raised when the output given by the trasducer function does not belong to the output alphabet
    """

    def __init__(self, symbols) -> None:
        super().__init__(f"The output tape given by the trasducer has symbols that are missing from it's output alphabet: {symbols}")
