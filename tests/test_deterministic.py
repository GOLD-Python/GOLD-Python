# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__
from gold_python import *  # noqa: F401


class TestDeterministic:  # noqa: D101
    def test_deterministic(self) -> None:
        @deltafunc
        def delta(state: int, symbol: str) -> tuple[int, int] | int:
            if state % 2 == 0:
                return (state, 2)
            return (state + 1) % 4

        @delta.register
        def _(state: int, extra: int, symbol: str) -> int:
            return (state + extra + 1) % 4

        states = [0, 1, 2, 3, [0, 2], [1, 2], [2, 2], [3, 2]]
        alphabet = ["a"]
        initial_state = 0
        final_states = [3]

        automata = DeterministicAutomata(
            states, alphabet, initial_state, final_states, delta
        )

        assert not automata.accepts_input("a")
        assert automata.accepts_input("aa")

    def test_transducer(self) -> None:
        @deltafunc
        def delta(state: int, _: str) -> tuple[int, int] | int:
            if state % 2 == 0:
                return (state, 2)
            return (state + 1) % 4

        @delta.register
        def _(state: int, extra: int, _: str) -> int:
            return (state + extra + 1) % 4

        @transducerfunc
        def trans(state: int, _: str) -> str:
            if state % 2 == 0:
                return "a"
            return "b"

        @trans.register
        def _(_: int, __: int, ___: str) -> str:
            return "c"

        states = [0, 1, 2, 3, [0, 2], [1, 2], [2, 2], [3, 2]]

        alphabet = ["a"]
        output_alphabet = ["a", "b", "c"]
        initial_state = 0
        final_states = [3]

        automata = DeterministicTrasducer(
            states, alphabet, output_alphabet, initial_state, final_states, delta, trans
        )

        assert automata.get_output("a")[0] == "a"
        assert automata.get_output("aa")[0] == "ac"
        assert automata.get_output("aaa")[0] == "acb"
