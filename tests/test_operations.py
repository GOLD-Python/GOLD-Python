# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__
from typing import Any  # noqa: F401
from gold_python.sets import *  # noqa: F401

class TestOperations:  # noqa: D101

    def test_between(self) -> None:
        """Test the between function."""
        assert len(between(0, 9)) == 10
        assert list(range(0, 10)) == between(0, 9)

    def test_product(self) -> None:
        """Test the product function."""
        assert len(product(between(0, 9), between(0, 9))) == 100
        assert len(product(between(0, 9), between(0, 9), between(0, 9))) == 1000
