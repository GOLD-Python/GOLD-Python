from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock
from typing import Any, Iterable, Set

from gold_python.deterministic import Function
from gold_python.util import call_func_iterable
from gold_python.exceptions import *
import networkx as nx

from anytree import Node
from anytree.exporter import DotExporter

class Task:
    def __init__(self, state: Any, tape: str, next: str, node: Node) -> None:
        self.state : Any = state
        self.tape : str = tape
        self.next : str = next
        self.node : Node = node

class PushdownTask(Task):

    def __init__(self, state, stack, tape, next, node) -> None:
        self.state = state
        self.stack = stack
        self.tape = tape
        self.next = next
        self.node = node

class TaskCounter:
    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.lock = Lock()

    def add_task(self) -> None:
        with self.lock:
            self.value += 1

    def finish_task(self) -> None:
        with self.lock:
            self.value -= 1

class NonDeterministicAutomata:

    def __init__(self, states: tuple, alphabet: Iterable, initial_state: tuple, final_states: tuple, delta: Function) -> None:
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.delta = delta
        self.network = nx.DiGraph()
        self.lock = Lock()

        self.end : Task | None = None

        self.network.add_nodes_from([str(state) for state in self.states])

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

    def acceptsInput(self, tape: str) -> tuple[bool, list]:

        if len(tape) == 0:
            return self.initial_state in self.final_states, []

        queue = Queue()
        counter = TaskCounter(2)

        for symbol in tape:
            if symbol not in self.alphabet:
                raise SymbolNotFoundException(symbol)

        root = Node((self.initial_state, tape))

        queue.put(Task(self.initial_state, tape, tape[0], root))
        queue.put(Task(self.initial_state, tape, "", root))

        stopped = False

        with ThreadPoolExecutor(max_workers=16) as executor:
            while counter.value != 0:
                task : Task | None = queue.get(block=True)
                if task is None:
                    stopped = True
                    break
                executor.submit(self.__acceptsInput, task, queue, counter)
            executor.shutdown(wait=False)
        if stopped:
            path = [(self.end.state, self.end.tape)] + [node.name for node in self.end.node.iter_path_reverse()]
            self.end = None
            return True, path
        else:
            return False, []

    def __insert_node(self, state, parent, next):
        with self.lock:
            node = Node(f"{state}, {next}", parent=parent)
        return node

    def __acceptsInput(self, task: Task, queue: Queue, counter: TaskCounter) -> None:

        node = self.__insert_node((task.state, task.tape), task.node, task.next if task.next != "" else "λ")

        if len(task.tape) == 0:
            if task.state in self.final_states:
                self.end = task
                queue.put(None)
            counter.finish_task()
            return

        try:
            nextStates = call_func_iterable(self.delta, task.state, task.next)
        except:
            counter.finish_task()
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
            counter.add_task()

            queue.put(lambda_task)
            counter.add_task()

        counter.finish_task()
