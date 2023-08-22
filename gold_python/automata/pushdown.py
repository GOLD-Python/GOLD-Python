from copy import deepcopy
from typing import Iterable, Callable
from gold_python.automata.nondeterministic import NonDeterministicAutomata


class AutomatonStack:
    def __init__(self):
        self.list = []

    def pop(self, *symbols):
        for symbol in symbols:
            if self.list.pop() != symbol:
                raise Exception(f"Expected symbol {symbol}, got something else instead")

    def push(self, *items):
        self.list.extend(items)

    def peek(self, *symbols):
        if len(symbols) > len(list):
            return False
        i = -1
        for symbol in symbols:
            if self.list[i] != symbol[i]:
                return False
            i -= 1
        return True

    def __size__(self):
        return len(self.list)

    def __str__(self) -> str:
        return f'"Stack: {self.list}'

    def __copy__(self):
        stack = AutomatonStack()
        stack.list = deepcopy(self.list)
        return stack


class PushdownAutomata(NonDeterministicAutomata):
    def __init__(
        self,
        states: tuple,
        alphabet: Iterable,
        initial_state: tuple,
        final_states: tuple,
        delta: Callable,
    ) -> None:
        super().__init__(states, alphabet, initial_state, final_states, delta)
