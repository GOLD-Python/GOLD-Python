"""
Utility functions for automata.

This module contains utility functions for automata.
"""
from typing import Callable, Any
from anytree import Node

from gold_python.delta import WrappedFunc

Function = WrappedFunc | Callable


class Task:
    def __init__(self, state: Any, tape: str, next: str, node: Node) -> None:
        self.state: Any = state
        self.tape: str = tape
        self.next: str = next
        self.node: Node = node


class PushdownTask(Task):
    def __init__(self, state, stack, tape, next, node) -> None:
        self.state = state
        self.stack = stack
        self.tape = tape
        self.next = next
        self.node = node
