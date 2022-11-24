from typing import Iterable
from gold_python.automata.util import Function
from abc import ABC, abstractclassmethod
from gold_python.exceptions import SymbolNotFoundException

from threading import Lock
import networkx as nx

class AbstractAutomata(ABC):

    def __init__(self, states: Iterable, alphabet: Iterable, initial_state: tuple, final_states: tuple, delta: Function) -> None:
        self.states = set([tuple(state) if isinstance(state, list) else state for state in states])
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta
        self.network = nx.DiGraph()

    def _inputAllowed(self, tape: str) -> bool:
        for symbol in tape:
            if symbol not in self.alphabet:
                raise SymbolNotFoundException(symbol)

    @abstractclassmethod
    def acceptsInput(self, tape: str) -> bool:
        pass

class AbstractNonDeterministicAutomata(AbstractAutomata):

    """Abstract class for non-deterministic automata."""

    def __init__(self, states: tuple, alphabet: Iterable, initial_state: tuple, final_states: tuple, delta: Function) -> None:
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta
        self.network = nx.DiGraph()
        self.lock = Lock()

        self.network.add_nodes_from([str(state) for state in self.states])

    @abstractclassmethod
    def _prepare_queue(self, queue):
        pass

    @abstractclassmethod
    def _insert_node(self, state, parent, next):
        pass
