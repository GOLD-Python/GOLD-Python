# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__
from typing import Any  # noqa: F401
from gold_python import *  # noqa: F401


class TestDelta:  # noqa: D101
    def test_deltafunc(self) -> None:  # noqa: D102
        @deltafunc
        def delta(_: Any, __: str) -> int:
            return 0

        @delta.register
        def _(_: Any, __: Any, ___: str) -> int:
            return 1

        assert delta(0, "a")[0] == 0
        assert delta(0, 0, "a")[0] == 1

    def test_transfunc(self) -> None:  # noqa: D102
        @transducerfunc
        def trans(_: Any, __: str) -> int:
            return 0

        @trans.register
        def _(_: Any, __: Any, ___: str) -> int:
            return 1

        assert trans(0, "a")[0] == 0
        assert trans(0, 0, "a")[0] == 1
