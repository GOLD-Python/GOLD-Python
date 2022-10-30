from collections import defaultdict
from inspect import signature
from typing import Any, Callable
from gold_python.exceptions import *
from gold_python.util import combine, combine_stack

class WrappedFunc:

    def __init__(self, func, combinefunc, minlen) -> None:
        self.__combinefunc = combinefunc
        self.__minlen = minlen
        self.__name = func.__name__
        self.__registry = defaultdict(list)
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

    def __init__(self) -> None:
        self.type = ""
        self.minlen = -1
        self.combinefunc = None

    def __call__(self, func: Callable) -> WrappedFunc:
        return WrappedFunc(func, self.combinefunc, self.minlen)

class DeltaDecorator(GoldDecorator):

    def __init__(self) -> None:
        super().__init__()
        self.type = 'deltafunc'
        self.minlen = 2
        self.combinefunc = combine

class TransducerDecorator(GoldDecorator):

    def __init__(self) -> None:
        super().__init__()
        self.type = 'transducerfunc'
        self.minlen = 2
        self.combinefunc = combine

class PushdownDecorator(GoldDecorator):

    def __init__(self) -> None:
        super().__init__()
        self.type = 'pushdownfunc'
        self.minlen = 3
        self.combinefunc = combine_stack


deltafunc = DeltaDecorator()
"""
Declares this function as a delta function for automata.

A delta function must have at least two arguments, and the last argument will
always be the next symbol. The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""

transducerfunc = TransducerDecorator()
"""
Declares this function as a transducer function for automata.

A transducer function must have at least two arguments, and the last argument will
always be the next symbol. The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""

pushdownfunc = PushdownDecorator()
"""
Declares this function as a pushdown function for pushdown automata.

A pushdown function must have at least three arguments, the last argument will
always be the next symbol, and the one before that is the current stack.
The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""
