"""
This module contains classes for deterministic automata.

The automatons in this module are deterministic, meaning that for each state and symbol, there is exactly one next state. Errors will be raised if this is not the case.

There is also a class for deterministic transducers, which are deterministic automata with output. The output is a string of symbols from an output alphabet, which is defined in the transducer.
"""

from collections import defaultdict
from typing import Iterable, Any, List, Tuple
import networkx as nx
from gold_python.exceptions import (
    PathNotFoundException,
    MultiplePathsFoundException,
    StateNotFoundException,
    OutputSymbolNotFoundException,
)
from gold_python.util import call_func_iterable
from gold_python.automata.util import Function
from gold_python.automata.abstract import AbstractAutomata


class DeterministicAutomata(AbstractAutomata):
    """
    Class for deterministic automata.

    This class is the base class for all deterministic automata.

    Args:
        states (Iterable): An iterable containing all states of the automata
        alphabet (Iterable): An iterable containing all symbols in the alphabet of the automata
        initial_state (Tuple | Any): The initial state of the automata
        final_states (Tuple | List): An iterable containing all final states of the automata
        delta (Function): A function that takes as input a state and a symbol and returns the next state of the automata

    The delta function will usually be decorated with the deltafunc decorator from the delta module.
    """

    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        initial_state: Tuple | Any,
        final_states: Tuple | List,
        delta: Function,
    ) -> None:
        # Convert states to a set of tuples if lists, otherwise leave them as is
        self.states = set(
            [tuple(state) if isinstance(state, list) else state for state in states]
        )
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta

        # Create network
        self.network = nx.DiGraph()
        self.network.add_nodes_from([str(state) for state in self.states])

        # Map to store edges between states
        edge_map = defaultdict(list)

        # Iterate through all states and symbols to create edges
        for state in self.states:
            for symbol in self.alphabet:
                nextStates = call_func_iterable(self.delta, state, symbol)

                if len(nextStates) < 1:
                    raise PathNotFoundException(symbol, state)
                elif len(nextStates) > 1:
                    raise MultiplePathsFoundException(symbol, state)

                if nextStates[0] not in self.states:
                    raise StateNotFoundException(symbol, state, nextStates[0])

                # Append symbol to edge and create a comma-separated list
                edge_map[str(state), str(nextStates[0])].append(symbol)
                symbol_list = ", ".join(edge_map[str(state), str(nextStates[0])])

                # Add edge to network
                self.network.add_edge(str(state), str(nextStates[0]), label=symbol_list)

    def accepts_input(self, tape: str) -> bool:
        self._input_allowed(tape)
        currentState = self.initial_state

        # Process each symbol in tape
        for symbol in tape:
            currentState = call_func_iterable(self.delta, currentState, symbol)[0]
            currentState = (
                tuple(currentState) if isinstance(currentState, list) else currentState
            )

        # Check if final state
        return currentState in self.final_states


class DeterministicTrasducer(DeterministicAutomata):
    """
    Class for deterministic transducers.

    This class defines a deterministic mealy transducer.

    Args:
        states (Iterable): An iterable containing all states of the transducer
        alphabet (Iterable): An iterable containing all symbols in the input alphabet of the transducer
        output_alphabet (Iterable): An iterable containing all symbols in the output alphabet of the transducer
        initial_state (Tuple | Any): The initial state of the transducer
        final_states (Tuple | List): An iterable containing all final states of the transducer
        delta (Function): A function that takes as input a state and a symbol and returns the next state of the transducer
        transfunc (Function): A function that takes as input a state and a symbol and returns the output of the transducer

    The delta and transfunc functions will usually be decorated with the deltafunc and transducerfunc decorators from the delta module.
    """

    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        output_alphabet: Iterable,
        initial_state: Tuple | Any,
        final_states: Tuple | List,
        delta: Function,
        transfunc: Function,
    ) -> None:
        # Initialize parent class
        super().__init__(states, alphabet, initial_state, final_states, delta)

        # Set output alphabet and transducer function
        self.output_alphabet = set(output_alphabet)
        self.transfunc = transfunc

    def get_output(self, tape: str) -> tuple[str, bool]:
        """
        Get the output of the transducer for the given input.

        Args:
            tape (str): The input tape
        Returns:
            tuple[str, bool]: A tuple containing the output tape and a boolean representing whether the transducer accepts the input

        If the transducer does not accept the input, the output tape will be an empty string.
        """
        self._input_allowed(tape)

        outputTape = ""
        currentState = self.initial_state

        # Process each symbol in tape, applying transducer function to each symbol
        for symbol in tape:
            outputTape += call_func_iterable(self.transfunc, currentState, symbol)[0]
            currentState = call_func_iterable(self.delta, currentState, symbol)[0]
            currentState = (
                tuple(currentState) if isinstance(currentState, list) else currentState
            )

        # Verify that all output symbols are in output alphabet
        if not set(outputTape).issubset(self.output_alphabet):
            raise OutputSymbolNotFoundException(
                self.output_alphabet.difference(outputTape)
            )

        # Check if final state
        return outputTape, currentState in self.final_states
