# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__
from gold_python import *
from gold_python.nondeterministic import NonDeterministicAutomata  # noqa: F401

class TestNonDeterministic:  # noqa: D101

    def test_nondeterministic(self) -> None:

        @deltafunc
        def delta(state: int, symbol: str) -> int:
            if symbol != "":
                return (state + 1) % 4

        @delta.register
        def _(state: int, symbol: str) -> int:
            if symbol != "":
                return (state + 2) % 4

        states = [0, 1, 2, 3]
        alphabet = ["a"]
        initial_state = 0
        final_states = [3]

        automata = NonDeterministicAutomata(states, alphabet, initial_state, final_states, delta)

        assert not automata.acceptsInput("")[0]
        assert not automata.acceptsInput("a")[0]
        assert automata.acceptsInput("aa")[0]
        assert automata.acceptsInput("aaa")[0]

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

        states = [0, 1, 2, 3, 4]
        alphabet = ["a"]
        initial_state = 0
        final_states = [4]

        automata = NonDeterministicAutomata(states, alphabet, initial_state, final_states, delta2)

        assert not automata.acceptsInput("")[0]
        assert not automata.acceptsInput("a")[0]
        assert automata.acceptsInput("aa")[0]
        assert automata.acceptsInput("aaa")[0]
