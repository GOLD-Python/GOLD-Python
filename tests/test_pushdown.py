# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__
from gold_python import *
from gold_python.automata.nondeterministic import NonDeterministicAutomata  # noqa: F401
from gold_python.automata.pushdown import AutomatonStack, PushdownAutomata  # noqa: F401


class TestPushdown:  # noqa: D101
    def test_pushdown(self) -> None:
        @pushdownfunc
        def delta(state: int, stack: AutomatonStack, symbol: str) -> int:
            if symbol == "":
                return 0

            if state == 0:
                stack.push(1)
                return 1
            if state == 1:
                stack.pop(1)
                return 2
            if state == 2:
                stack.pop(1, 1)
                return 3
            if state == 3:
                stack.pop(1)

            raise Exception("No path found")

        @delta.register
        def _(state: int, stack: AutomatonStack, symbol: str) -> int:
            if symbol == "":
                return 0

            if state == 1:
                stack.push(1)
                return 2

            raise Exception("No path found")

        states = [0, 1, 2, 3]
        alphabet = ["a"]
        initial_state = 0
        final_states = [3]

        automata = PushdownAutomata(
            states, alphabet, initial_state, final_states, delta
        )

        assert not automata.accepts_input("")
        assert not automata.accepts_input("a")
        assert not automata.accepts_input("aa")
        assert automata.accepts_input("aaa")
