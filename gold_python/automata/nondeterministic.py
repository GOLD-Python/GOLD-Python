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


# TODO: Re-implement multi-core support. Current implementation is cleaner, but unstable
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

        edge_map = defaultdict(list)

        for state in self.states:
            for symbol in self.alphabet:
                nextStates = set(call_func_iterable(self.delta, state, symbol))

                if not nextStates.issubset(self.states):
                    raise StateNotFoundException(symbol, state, nextStates)

                for nextState in nextStates:
                    edge_map[str(state), str(nextState)].append(symbol)
                    symbol_list = ", ".join(edge_map[str(state), str(nextState)])
                    self.network.add_edge(str(state), str(nextState), label=symbol_list)

    def acceptsInput(self, tape: str) -> bool:
        return self.acceptsInputPath(tape)[0]

    def acceptsInputPath(self, tape: str) -> tuple[bool, list]:
        """
        May god have mercy on my soul
        """
        if len(tape) == 0:
            return self.initial_state in self.final_states, []

        queue: Queue = Queue()
        return_queue: Queue = Queue(1)
        counter = TaskCounter(0)

        self._inputAllowed(tape)

        root = Node((self.initial_state, tape))
        self._prepare_queue(root, tape, queue)

        """
        TODO: Remove this comment when multi-core support is re-implemented

        with ProcessPoolExecutor(max_workers=16) as executor:
            while True:
                task : Task | None = queue.get(block=True, timeout=0.5)
                if task is None:
                    if counter.value != 0:
                        break
                    else:
                        continue
                executor.submit(self.__acceptsInput, task, queue, return_queue, counter)
                counter.add_task()
            executor.shutdown(wait=False)
        """

        while True:
            task: Task | None = queue.get(block=True, timeout=0.5)
            if task is None:
                if counter.value != 0:
                    break
                else:
                    continue
            if return_queue.qsize() != 0:
                break
            self.__acceptsInput(task, queue, return_queue, counter)

        # DotExporter(root).to_picture("result.png")

        if return_queue.full():
            final_state: Task = return_queue.get_nowait()
            path = [(final_state.state, final_state.tape)] + [
                node.name for node in final_state.node.iter_path_reverse()
            ]
            return True, path
        else:
            return False, []

    def _prepare_queue(self, root: Node, tape: str, queue: Queue):
        queue.put(Task(self.initial_state, tape, tape[0], root))
        queue.put(Task(self.initial_state, tape, "", root))

    def _insert_node(self, state: Any, parent, next):
        with self.lock:
            node = Node(f"{state}, {next}", parent=parent)
        return node

    def __acceptsInput(
        self, task: Task, queue: Queue, return_queue: Queue, counter: TaskCounter
    ) -> None:
        node = self._insert_node(
            (task.state, task.tape), task.node, task.next if task.next != "" else "λ"
        )

        if len(task.tape) == 0:
            if task.state in self.final_states:
                return_queue.put_nowait(task)
            counter.finish_task()
            queue.put(None)
            return

        try:
            nextStates = call_func_iterable(self.delta, task.state, task.next)
            # pylint: disable=bare-except
        except:
            counter.finish_task()
            queue.put(None)
            return

        for state in set(nextStates):
            if task.next == "":
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

        counter.finish_task()
