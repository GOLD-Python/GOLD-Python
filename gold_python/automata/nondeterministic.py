from collections import defaultdict
from queue import Queue
from threading import Lock
from typing import Iterable, Any

from anytree import Node

from gold_python.automata.deterministic import Function
from gold_python.util import call_func_iterable
from gold_python.exceptions import StateNotFoundException
from gold_python.automata.abstract import AbstractNonDeterministicAutomata
from gold_python.automata.util import Task


class TaskCounter:
    """
    Task counter for multi-core support
    """

    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.lock = Lock()

    def add_tasks(self, num: int) -> None:
        """
        Add tasks to task counter
        """
        with self.lock:
            self.value += num

    def finish_task(self) -> None:
        """
        Finish task on task counter
        """
        with self.lock:
            self.value -= 1


# TODO: Re-implement multi-core support. Current implementation is cleaner, but slower.
class NonDeterministicAutomata(AbstractNonDeterministicAutomata):
    def __init__(
        self,
        states: Iterable,
        alphabet: Iterable,
        initial_state: tuple | Any,
        final_states: tuple | list,
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

    def accepts_input_path(self, tape: str) -> tuple[bool, list]:
        if len(tape) == 0:
            return self.initial_state in self.final_states, []

        # Create queue for tasks and a return queue to check if a path has been found
        queue: Queue = Queue()
        return_queue: Queue = Queue(1)
        counter = TaskCounter(0)

        self._input_allowed(tape)

        # Create root node, and add tasks to queue
        root = Node((self.initial_state, tape))
        self._prepare_queue(root, tape, queue)

        # Main loop to process tasks
        while True:
            # Get task from queue
            task: Task | None = queue.get(block=True, timeout=0.5)
            if task is None:
                if counter.value != 0:
                    break
                else:
                    continue
            if return_queue.qsize() != 0:
                break
            # Process task
            self.__accepts_input(task, queue, return_queue, counter)

        # Check if path has been found, and construct path if it has
        if return_queue.full():
            final_state: Task = return_queue.get_nowait()
            path = [(final_state.state, final_state.tape)] + [
                node.name for node in final_state.node.iter_path_reverse()
            ]
            return True, path
        else:
            return False, []

    def _prepare_queue(self, root: Node, tape: str, queue: Queue):
        # Add initial tasks to queue, including lambda transitions
        queue.put(Task(self.initial_state, tape, tape[0], root))
        queue.put(Task(self.initial_state, tape, "", root))

    def _insert_node(self, state: Any, parent, next):
        # Insert node into tree using lock, and return node
        with self.lock:
            node = Node(f"{state}, {next}", parent=parent)
        return node

    def __accepts_input(
        self, task: Task, queue: Queue, return_queue: Queue, counter: TaskCounter
    ) -> None:
        # Insert node into tree, if empty transition, insert lambda symbol
        node = self._insert_node(
            (task.state, task.tape), task.node, task.next if task.next != "" else "λ"
        )

        # Finish task if tape is empty, and add to return queue if final state
        if len(task.tape) == 0:
            if task.state in self.final_states:
                return_queue.put_nowait(task)
            counter.finish_task()
            queue.put(None)
            return

        # Get next states from delta function, and create tasks for each state
        # NOTE: Any exceptions raised here will be interpreted as no path found
        try:
            nextStates = call_func_iterable(self.delta, task.state, task.next)
        except:
            counter.finish_task()
            queue.put(None)
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

            queue.put(continue_task)
            queue.put(lambda_task)
            counter.add_tasks(2)

        # Finish current task
        counter.finish_task()
