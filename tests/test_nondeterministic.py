# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__
from gold_python import *
from gold_python.automata.nondeterministic import NonDeterministicAutomata  # noqa: F401


class TestNonDeterministic:  # noqa: D101
    def test_nondeterministic(self) -> None:
        @deltafunc
        def delta(state: int, symbol: str) -> int:
            if symbol != "":
                return (state + 1) % 4
            raise Exception("No path found")

        @delta.register
        def _(state: int, symbol: str) -> int:
            if symbol != "":
                return (state + 2) % 4
            raise Exception("No path found")

        states = [0, 1, 2, 3]
        alphabet = ["a"]
        initial_state = 0
        final_states = [3]

        automata = NonDeterministicAutomata(
            states, alphabet, initial_state, final_states, delta
        )

        assert not automata.accepts_input("")
        assert not automata.accepts_input("a")
        assert automata.accepts_input("aa")
        assert automata.accepts_input("aaa")

        @deltafunc
        def delta2(state: int, symbol: str) -> int:
            if symbol != "":
                return (state + 1) % 5
            else:
                return 3

        @delta2.register
        def _(state: int, symbol: str) -> int:
            if symbol != "":
                return (state + 2) % 5
            raise Exception("No path found")

        states = [0, 1, 2, 3, 4]
        alphabet = ["a"]
        initial_state = 0
        final_states = [4]

        automata = NonDeterministicAutomata(
            states, alphabet, initial_state, final_states, delta2
        )

        assert not automata.accepts_input("")
        assert automata.accepts_input("a")
        assert automata.accepts_input("aa")
        assert automata.accepts_input("aaa")
