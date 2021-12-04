import itertools
import json
from dataclasses import field
from heapq import *
from typing import Callable, Generator, Iterator, Union

from common.environment import Environment
from common.experiment import Example
from common.prorgam import Program
from common.tokens.control_tokens import RecursiveCallLimitReached, LoopIterationLimitReached
from common.tokens.pixel_tokens import *
from search.abstract_search import SearchAlgorithm
from search.invent import invent2
from search.search_result import SearchResult

MAX_NUMBER_OF_ITERATIONS = 20
MAX_TOKEN_FUNCTION_DEPTH = 3


@dataclass(init=True, order=True)
class Node:
    priority: float  # TODO: make sure these are always int
    count: int
    item: any = field(compare=False)


class UniquePriorityQueue:

    def __init__(self):
        self.heap: list[Node] = list()
        self.item_set: dict[any, Union[Node, None]] = dict()
        self.count = itertools.count()

    def insert(self, item: any, priority: float) -> bool:
        """
        Inserts item with given priority in queue or update the priority if the item is already present.
        @param item: Object to insert in the queue
        @param priority: Items with a lower priority will be popped first
        @return: True if item was already present and updated, False otherwise
        """
        updated = False
        if item in self.item_set:
            self.item_set[item].item = None
            updated = True
        new_node = Node(priority, next(self.count), item)
        heappush(self.heap, new_node)
        self.item_set[item] = new_node
        return updated

    def pop(self) -> Union[tuple[any, float], None]:
        """
        Removes and returns item with lowest priority.
        If the lowest priority is shared by two items, returns last added item
        @return: Tuple consisting of item with lowest priority and the value of priority
        """
        while self.heap:
            node = heappop(self.heap)
            if node.item is not None:
                self.item_set.pop(node.item)
                return node.item, node.priority
        raise IndexError("Queue is empty.")

    def __bool__(self):
        """
        Returns whether the queue has items
        @return: True if queue contains one or more items, False otherwise.
        """
        while self.heap and self.heap[0].item is None:
            heappop(self.heap)
        return bool(self.heap)


class AStar(SearchAlgorithm):

    def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
        self.input_envs: tuple[Environment] = tuple(e.input_environment for e in training_examples)
        self.output_envs: tuple[Environment] = tuple(e.output_environment for e in training_examples)
        self.tokens: list[Token] = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)
        self.loss_function: Callable[[int, int], int] = lambda g, h: g + h
        self.program_generator: Iterator[Union[Program, None]] = self.best_first_search_upq(
            self.input_envs, self.output_envs, self.tokens, self.loss_function, self._heuristic_min)
        self._expanded_programs: list[Program] = list()

    def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
        try:
            if p := next(self.program_generator):
                # a solution was found: record solution and stop iterating
                self._best_program = p
                return False
            # no solution found yet: continue iterating
            return True
        except StopIteration:
            # nothing left to explore: stop iterating (will never happen)
            return False


    def extend_result(self, search_result: SearchResult):
        search_result.dictionary['expanded_programs'] = self._expanded_programs
        return search_result

    @staticmethod
    def _correct(from_states: tuple[Environment], to_states: tuple[Environment]) -> bool:
        return all(map(lambda tup: tup[0].correct(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _heuristic(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return sum(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states))) / len(from_states)

    @staticmethod
    def _heuristic_min(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return min(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _find_program(node, reached):
        sequence = []
        while reached[node][1]:
            sequence.append(reached[node][2])
            node = reached[node][1]
        sequence.reverse()
        return Program(sequence)

    def best_first_search_upq(self, start_node: tuple[Environment], end_node: tuple[Environment],
                              tokens: list[Token], f, h) -> Iterator[Program]:
        if self._correct(start_node, end_node):
            yield Program([])
        reached = {start_node: (0, False, False)}  # for each reached node: (path_cost, previous_node, token_used)
        queue = UniquePriorityQueue()
        gcost = 0
        hcost = h(start_node, end_node)
        fcost = f(gcost, hcost)
        queue.insert(start_node, fcost)
        node = None
        while queue:
            node, fcost = queue.pop()
            gcost, _, _ = reached[node]
            # self._expanded_programs.append(self._find_program(node, reached))
            solution = None
            node_copies = [copy.deepcopy(node) for _ in tokens]
            for token, node_copy in zip(tokens, node_copies):
                try:
                    child = tuple(map(token.apply, node_copy))
                    if solution is None and self._correct(child, end_node):
                        solution = child  # check early if we've found a solution
                    gcost_child = gcost + token.number_of_tokens()
                    # if child was not yet expanded or our new gcost is the smallest up until now
                    if child not in reached or gcost_child < reached[child][0]:
                        reached[child] = gcost_child, node, token
                        hcost_child = h(child, end_node)
                        fcost_child = f(gcost_child, hcost_child)
                        queue.insert(child, fcost_child)
                except(InvalidTransition, RecursiveCallLimitReached, LoopIterationLimitReached):
                    pass
            if solution:
                yield self._find_program(solution, reached)
            else:
                yield None
        return
