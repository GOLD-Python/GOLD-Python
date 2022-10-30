from collections import defaultdict
from typing import Callable, Iterable
import networkx as nx
from gold_python.delta import WrappedFunc
from gold_python.exceptions import *
from gold_python.util import call_func_iterable

Function = WrappedFunc | Callable

class DeterministicAutomata:

    def __init__(self, states: Iterable, alphabet: Iterable, initial_state: tuple, final_states: tuple, delta: Function) -> None:
        self.states = set([tuple(state) if isinstance(state, list) else state for state in states])
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta
        self.network = nx.DiGraph()

        self.network.add_nodes_from([str(state) for state in self.states])

        edge_map = defaultdict(list)

        for state in self.states:
            for symbol in self.alphabet:
                nextStates = call_func_iterable(self.delta, state, symbol)

                if len(nextStates) < 1:
                    raise PathNotFoundException(symbol, state)
                elif len(nextStates) > 1:
                    raise MultiplePathsFoundException(symbol, state)

                if nextStates[0] not in self.states:
                    raise StateNotFoundException(symbol, state, nextStates[0])

                edge_map[str(state), str(nextStates[0])].append(symbol)

                symbol_list = ", ".join(edge_map[str(state), str(nextStates[0])])

                self.network.add_edge(str(state), str(nextStates[0]), label=symbol_list)

    def inputAllowed(self, tape: str) -> bool:
        for symbol in tape:
            if symbol not in self.alphabet:
                raise SymbolNotFoundException(symbol)

    def acceptsInput(self, tape: str) -> bool:

        self.inputAllowed(tape)

        currentState = self.initial_state

        for symbol in tape:
            currentState = call_func_iterable(self.delta, currentState, symbol)[0]

            currentState = tuple(currentState) if isinstance(currentState, list) else currentState

        return currentState in self.final_states

class DeterministicTrasducer(DeterministicAutomata):

    def __init__(self, states: Iterable, alphabet: Iterable, output_alphabet: Iterable, initial_state: tuple, final_states: tuple, delta: Function, transfunc: Function) -> None:

        super().__init__(states, alphabet, initial_state, final_states, delta)
        self.output_alphabet = set(output_alphabet)
        self.transfunc = transfunc

    def getOutput(self, tape: str) -> tuple[str, bool]:

        self.inputAllowed(tape)

        outputTape = ""
        currentState = self.initial_state

        for symbol in tape:
            outputTape += call_func_iterable(self.transfunc, currentState, symbol)[0]
            currentState = call_func_iterable(self.delta, currentState, symbol)[0]
            currentState = tuple(currentState) if isinstance(currentState, list) else currentState

        if not set(outputTape).issubset(self.output_alphabet):
            raise OutputSymbolNotFoundException(self.output_alphabet.difference(outputTape))

        return outputTape, currentState in self.final_states
