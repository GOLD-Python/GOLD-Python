"""
This module defines a pushdown automata class.

A pushdown automata is a non-deterministic automata with a stack that
can store symbols. It can push symbols onto the stack, pop symbols from the stack,
and check if the top of the stack contains certain symbols. Do take in mind
that pop operations must give the symbols that are popped, and that the stack
will throw an exception if the wrong symbol is popped. Adittionally, the stack
must be empty for the automata to accept the input.
"""

from copy import deepcopy
from typing import Iterable, Tuple, Any, List, Callable

from anytree import Node

from gold_python.automata.abstract import AbstractNonDeterministicAutomata
from gold_python.automata.nondeterministic import _Queue
from gold_python.exceptions import WrongSymbolException
from gold_python.util import call_func_iterable
from gold_python.automata.util import PushdownTask, Task

EMPTY_TRANSITION = ""


class AutomatonStack:
    """
    Class for a stack used in a pushdown automata.

    This class is used to represent the stack of a pushdown automata. Do take in mind
    that pop operations must give the symbols that are popped, and that the stack
    will throw an exception if the wrong symbol is popped.
    """

    def __init__(self):
        self.list = []

    def pop(self, *symbols):
        """
        Pop symbols from the stack.

        Args:
            symbols (str): The symbols to pop from the stack
        Raises:
            WrongSymbolException: If the wrong symbol is popped from the stack
        """
        for symbol in symbols:
            obtained = self.list.pop()
            if obtained != symbol:
                raise WrongSymbolException(obtained, symbol)

    def push(self, *items):
        """
        Push symbols onto the stack.

        Args:
            items (str): The symbols to push onto the stack
        """
        self.list.extend(items)

    def peek(self, *symbols):
        """
        Check if the top of the stack contains certain symbols.

        Args:
            symbols (str): The symbols to check for
        """
        if len(symbols) > len(list):
            return False
        i = -1
        for symbol in symbols:
            if self.list[i] != symbol[i]:
                return False
            i -= 1
        return True

    def __len__(self):
        return len(self.list)

    def __size__(self):
        return len(self.list)

    def __str__(self) -> str:
        return f'"Stack: {self.list}'

    def __copy__(self):
        stack = AutomatonStack()
        stack.list = deepcopy(self.list)
        return stack


class PushdownAutomata(AbstractNonDeterministicAutomata):
    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        initial_state: Tuple | Any,
        final_states: Tuple | List,
        delta: Callable,
    ) -> None:
        super().__init__(states, alphabet, initial_state, final_states, delta)

        # TODO: Network will be used for visualization, so implement it

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
            task: PushdownTask | None = queue.dequeue()
            if task is None:
                break

            self._run_task_stack(task, queue, return_queue)

        # Check if path has been found, and construct path if it has
        if return_queue.peek() is not None:
            final_state: PushdownTask = return_queue.dequeue()
            path = [(final_state.state, final_state.tape, final_state.stack)] + [
                node.name for node in final_state.node.iter_path_reverse()
            ]
            return True, path
        else:
            return False, []

    def _prepare_queue(self, root: Node, tape: str, queue: _Queue):
        # Add initial tasks to queue, including lambda transitions
        queue.enqueue(
            PushdownTask(self.initial_state, AutomatonStack(), tape, tape[0], root)
        )
        queue.enqueue(
            PushdownTask(self.initial_state, AutomatonStack(), tape, "", root)
        )

    def _insert_node(self, state: Any, parent: Node, next: str):
        return self._insert_node_stack(state, AutomatonStack(), parent, next)

    def _insert_node_stack(
        self, state: Any, stack: AutomatonStack, parent: Node, next: str
    ):
        # Insert node into tree using lock, and return node

        lambda_next = next if next != EMPTY_TRANSITION else "λ"
        display_text = f"{state}, {stack}, {lambda_next}"
        with self.lock:
            node = Node(display_text, parent=parent)
        return node

    def _run_task(self, task: Task, queue: _Queue, return_queue: _Queue) -> None:
        self._run_task_stack(
            PushdownTask(task.state, AutomatonStack(), task.tape, task.next, task.node),
            queue,
            return_queue,
        )

    def _run_task_stack(
        self,
        task: PushdownTask,
        queue: _Queue,
        return_queue: _Queue,
    ) -> None:
        # Insert node into tree, if empty transition, insert lambda symbol
        node = self._insert_node_stack(
            (task.state, task.tape), task.stack, task.node, task.next
        )

        # Finish task if tape is empty, and add to return queue if final state
        if len(task.tape) == 0:
            if task.state in self.final_states and len(task.stack) == 0:
                return_queue.enqueue(task)
            return
        # Exception handling is done in delta function, so no need to check for exceptions here
        nextStates = call_func_iterable(self.delta, task.state, task.stack, task.next)

        # Add tasks to queue, and increment task counter. Increment task counter by 2, since each task creates 2 new tasks, one for the next symbol, and one for lambda transition
        for state, stack in set(nextStates):
            if task.next == EMPTY_TRANSITION:
                # If empty transition, don't add lambda transition, to avoid infinite loops
                if task.state == state:
                    continue
                continue_task = PushdownTask(
                    state, stack, task.tape, task.tape[0], node
                )
                lambda_task = PushdownTask(state, stack, task.tape, "", node)
            else:
                next_symbol = EMPTY_TRANSITION if len(task.tape) == 1 else task.tape[1]
                next_tape = task.tape[1:]

                continue_task = PushdownTask(state, stack, next_tape, next_symbol, node)
                lambda_task = PushdownTask(state, stack, next_tape, "", node)

            queue.enqueue(continue_task)
            queue.enqueue(lambda_task)
