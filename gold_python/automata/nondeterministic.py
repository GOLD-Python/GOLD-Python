"""
This module defines a non-deterministic automata class.

Unlike the deterministic automata class, a non-deterministic automata can have multiple transitions for a given state and symbol. This is represented by a set of next states for each state and symbol. It also has a lambda transition, which is represented by an empty string as the symbol in the delta function.
"""

from collections import defaultdict, deque
from typing import Iterable, Any, Tuple, List

from anytree import Node

from gold_python.automata.deterministic import Function
from gold_python.util import call_func_iterable
from gold_python.exceptions import StateNotFoundException
from gold_python.automata.abstract import AbstractNonDeterministicAutomata
from gold_python.automata.util import Task


class _Queue:
    def __init__(self, len=None):
        self.queue = deque(maxlen=len)

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None  # Return None when the queue is empty

    def peek(self):
        if self.queue:
            return self.queue[0]
        else:
            return None  # Return None when the queue is empty

    def __len__(self):
        return len(self.queue)


# TODO: Re-implement multi-core support. Current implementation is cleaner, but slower.
class NonDeterministicAutomata(AbstractNonDeterministicAutomata):
    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        initial_state: Tuple | Any,
        final_states: Tuple | List,
        delta: Function,
    ) -> None:
        super().__init__(states, alphabet, initial_state, final_states, delta)

        # Map to store edges between states
        edge_map = defaultdict(list)

        # Iterate through all states and symbols to create edges
        for state in self.states:
            for symbol in self.alphabet:
                nextStates = set(call_func_iterable(self.delta, state, symbol))

                if not nextStates.issubset(self.states):
                    raise StateNotFoundException(symbol, state, nextStates)

                for nextState in nextStates:
                    edge_map[str(state), str(nextState)].append(symbol)
                    symbol_list = ", ".join(edge_map[str(state), str(nextState)])
                    self.network.add_edge(str(state), str(nextState), label=symbol_list)

    def accepts_input(self, tape: str) -> bool:
        return self.accepts_input_path(tape)[0]

    def accepts_input_path(self, tape: str) -> Tuple[bool, List]:
        """
        Check if the automata accepts the given input, and return the path if it does.

        Args:
            tape (str): The input string to check
        Returns:
            Tuple[bool, List]: A tuple containing a boolean representing if the automata accepts the input, and a list containing the path taken by the automata if it accepts the input.

        This is a separate method from accepts_input, since it returns the path taken by the automata if it accepts the input.
        """
        if len(tape) == 0:
            return self.initial_state in self.final_states, []

        # Create queue for tasks and a return queue to check if a path has been found

        queue: _Queue = _Queue()
        return_queue: _Queue = _Queue(1)

        self._input_allowed(tape)

        # Create root node, and add tasks to queue
        root = Node((self.initial_state, tape))
        self._prepare_queue(root, tape, queue)

        # Main loop to process tasks
        while True:
            # Get task from queue
            finished = return_queue.peek()
            if finished is not None:
                break
            task: Task | None = queue.dequeue()
            if task is None:
                break

            self._run_task(task, queue, return_queue)

        # Check if path has been found, and construct path if it has
        if return_queue.peek() is not None:
            final_state: Task = return_queue.dequeue()
            path = [(final_state.state, final_state.tape)] + [
                node.name for node in final_state.node.iter_path_reverse()
            ]
            return True, path
        else:
            return False, []

    def _prepare_queue(self, root: Node, tape: str, queue: _Queue):
        # Add initial tasks to queue, including lambda transitions
        queue.enqueue(Task(self.initial_state, tape, tape[0], root))
        queue.enqueue(Task(self.initial_state, tape, "", root))

    def _insert_node(self, state: Any, parent, next):
        # Insert node into tree using lock, and return node
        with self.lock:
            node = Node(f"{state}, {next}", parent=parent)
        return node

    def _run_task(
        self,
        task: Task,
        queue: _Queue,
        return_queue: _Queue,
    ) -> None:
        # Insert node into tree, if empty transition, insert lambda symbol
        node = self._insert_node(
            (task.state, task.tape), task.node, task.next if task.next != "" else "λ"
        )

        # Finish task if tape is empty, and add to return queue if final state
        if len(task.tape) == 0:
            if task.state in self.final_states:
                return_queue.enqueue(task)
            return

        # Get next states from delta function, and create tasks for each state
        # NOTE: Any exceptions raised here will be interpreted as no path found
        try:
            nextStates = call_func_iterable(self.delta, task.state, task.next)
        except:
            return

        # Add tasks to queue, and increment task counter. Increment task counter by 2, since each task creates 2 new tasks, one for the next symbol, and one for lambda transition
        for state in set(nextStates):
            if task.next == "":
                # If empty transition, don't add lambda transition, to avoid infinite loops
                if task.state == state:
                    continue
                continue_task = Task(state, task.tape, task.tape[0], node)
                lambda_task = Task(state, task.tape, "", node)
            else:
                next_symbol = "" if len(task.tape) == 1 else task.tape[1]
                next_tape = task.tape[1:]

                continue_task = Task(state, next_tape, next_symbol, node)
                lambda_task = Task(state, next_tape, "", node)

            queue.enqueue(continue_task)
            queue.enqueue(lambda_task)
