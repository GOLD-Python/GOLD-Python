"""
This module contains decorators for declaring functions as delta functions
for automata.

The delta functions are used by the automata classes in the automata module
to determine the next state of the automata.
"""

from collections import defaultdict
from inspect import signature
from typing import Any, Callable
from gold_python.exceptions import (
    NotEnoughArgumentsException,
    FunctionDefinitionNotFoundException,
)
from gold_python.util import combine, combine_stack


class WrappedFunc:
    """
    A wrapper class for functions that are callable by delta-like functions

    This class is not meant to be used directly, but rather instantiated by
    the decorators in this module.
    """

    def __init__(self, func, combinefunc, minlen) -> None:
        self.__combinefunc = combinefunc
        self.__minlen = minlen
        self.__name = func.__name__
        self.__registry: dict = defaultdict(list)
        self.register(func)

    def register(self, func: Callable):
        """
        Registers this function as callable by a delta-like function
        """
        paramLength = len(signature(func).parameters)
        self.__registry[paramLength].append(func)
        return func

    def __call__(self, *args: Any) -> list:
        if len(args) < self.__minlen:
            raise NotEnoughArgumentsException(self.__name)

        if len(self.__registry[len(args)]) < 1:
            raise FunctionDefinitionNotFoundException(self.__name, len(args))

        return self.__combinefunc(self.__registry[len(args)], *args)


class GoldDecorator:
    """
    Base class for all decorators in this module

    This class is not meant to be used directly, but rather subclassed
    by the decorators in this module.
    """

    def __init__(
        self, decorator_type: str, min_len: int, combine_func: Callable
    ) -> None:
        self.decorator_type = decorator_type
        self.min_len = min_len
        self.combine_func = combine_func

    def __repr__(self) -> str:
        return f"<{self.decorator_type} decorator>"

    def __call__(self, func: Callable) -> WrappedFunc:
        return WrappedFunc(func, self.combine_func, self.min_len)


deltafunc = GoldDecorator("deltafunc", 2, combine)
"""
Declares this function as a delta function for automata.

A delta function must have at least two arguments, and the last argument will
always be the next symbol. The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""

transducerfunc = GoldDecorator("transducerfunc", 2, combine)
"""
Declares this function as a transducer function for automata.

A transducer function must have at least two arguments, and the last argument will
always be the next symbol. The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""

pushdownfunc = GoldDecorator("pushdownfunc", 3, combine_stack)
"""
Declares this function as a pushdown function for pushdown automata.

A pushdown function must have at least three arguments, the last argument will
always be the next symbol, and the one before that is the current stack.
The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""
