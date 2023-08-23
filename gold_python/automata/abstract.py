from typing import Iterable, Any
from threading import Lock
import networkx as nx
from anytree import Node
import abc

from gold_python.exceptions import SymbolNotFoundException
from gold_python.automata.util import Function


class AbstractAutomata(abc.ABC):
    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        initial_state: tuple | Any,
        final_states: tuple | list,
        delta: Function,
    ) -> None:
        self.states = set(
            [tuple(state) if isinstance(state, list) else state for state in states]
        )
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta
        self.network = nx.DiGraph()

    def _input_allowed(self, tape: str) -> None:
        for symbol in tape:
            if symbol not in self.alphabet:
                raise SymbolNotFoundException(symbol)

    @abc.abstractmethod
    def accepts_input(self, tape: str) -> bool:
        pass


class AbstractNonDeterministicAutomata(AbstractAutomata):

    """Abstract class for non-deterministic automata."""

    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        initial_state: tuple | Any,
        final_states: tuple | list,
        delta: Function,
    ) -> None:
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta
        self.network = nx.DiGraph()
        self.lock = Lock()

        self.network.add_nodes_from([str(state) for state in self.states])

    @abc.abstractmethod
    def _prepare_queue(self, root: Node, tape: str, queue):
        pass

    @abc.abstractmethod
    def _insert_node(self, state, parent, next):
        pass
