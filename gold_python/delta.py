from inspect import signature
from typing import Any, Callable
from util import *

class WrappedFunc:

    def __init__(self, combinefunc) -> None:
        self.__combinefunc = combinefunc
        self.__registry = {}

    def register(self, func: Callable):
        """
        Registers this function as callable by a delta-like function
        """
        paramLength = len(signature(func).parameters)

        if paramLength in self.__registry:
            self.__registry[paramLength].append(func)
        else:
            self.__registry[paramLength] = [func,]
        return func

    def __call__(self, *args: Any) -> Any:
        if len(args) < self.minlen:
            raise Exception("Delta function must have at least two parameters to be valid")

        if len(args) not in self.__registry:
            raise Exception(f"Could not find a function for a state that contains {len(args)} elements")

        return self.__combinefunc(self.__registry[len(args)], *args)()


class DeltaFunc:

    def __init__(self) -> None:
        self.type = 'deltafunc'
        self.minlen = 2
        self.combinefunc = combine

    def __call__(self, func: Callable) -> WrappedFunc:
        wrapperFunc = WrappedFunc(self.combinefunc)
        wrapperFunc.register(func)
        return wrapperFunc

class TransducerFunc(DeltaFunc):

    def __init__(self) -> None:
        super().__init__()
        self.type = 'transducerfunc'

class PushdownFunc(DeltaFunc):

    def __init__(self) -> None:
        super().__init__()
        self.type = 'pushdownfunc'
        self.minlen = 3
        self.combinefunc = combine_stack


deltafunc = DeltaFunc()
"""
Declares this function as a delta function for automata.

A delta function must have at least two arguments, and the last argument will
always be the next symbol. The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""

transducerfunc = TransducerFunc()
"""
Declares this function as a transducer function for automata.

A transducer function must have at least two arguments, and the last argument will
always be the next symbol. The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""

pushdownfunc = PushdownFunc()
"""
Declares this function as a pushdown function for pushdown automata.

A pushdown function must have at least three arguments, the last argument will
always be the next symbol, and the one before that is the current stack.
The other arguments before that will be the current state,
split into variables if the state is a tuple.
"""
