from typing import Iterator, List, Union

from common.experiment import Example
from common.prorgam import Program
from common.tokens.control_tokens import LoopIterationLimitReached
from common.tokens.pixel_tokens import *
from search.a_star.unique_priority_queue import UniquePriorityQueue
from search.abstract_search import SearchAlgorithm
from search.invent import invent2
from search.search_result import SearchResult

MAX_TOKEN_FUNCTION_DEPTH = 3


class AStar(SearchAlgorithm):
    def __init__(self, time_limit_sec: float, weight: int = False):
        super().__init__(time_limit_sec)
        if weight is False:
            weight = 0.5
        assert 0 <= weight <= 1
        self.weight = weight

    @property
    def best_program(self) -> Program:
        return self._find_program(self._best_program_node, self.reached)

    @property
    def best_f_program(self) -> Program:
        return self._find_program(self._best_f_program_node, self.reached)

    def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
        self.loss_function = lambda g, h: self.weight * g + (1-self.weight) * h
        self.heuristic = self._heuristic_mean
        self.input_envs: tuple[Environment] = tuple(e.input_environment for e in training_examples)
        self.output_envs: tuple[Environment] = tuple(e.output_environment for e in training_examples)
        self.tokens: list[Token] = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)
        self.number_of_iterations: int = 0
        self._best_cost = float('inf')
        self._best_f_cost = float('inf')
        self.reached = {}
        self._solution_found = False
        self._best_program_node = None
        self._best_f_program_node = None
        self.g_cost_per_iteration = []   # (iteration_number, g_cost)
        self.cost_per_iteration = []  # (iteration_number, h_cost)
        self.program_generator: Iterator[Union[Program, None]] = self.best_first_search_upq(
            self.input_envs, self.output_envs, self.tokens, self.loss_function, self.heuristic)

    def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
        try:
            if node := next(self.program_generator):
                # a solution was found: stop iterating
                self._solution_found = True
                return False
            # no solution found yet: continue iterating
            return True
        except StopIteration:
            # nothing left to explore: stop iterating (will never happen)
            return False

    def extend_result(self, search_result: SearchResult):
        search_result.dictionary['solution_found'] = self._solution_found
        search_result.dictionary['best_f_program'] = str(self.best_f_program)
        search_result.dictionary['g_cost_per_iteration'] = self.g_cost_per_iteration
        search_result.dictionary['heuristic'] = self.heuristic.__name__
        search_result.dictionary['weight'] = self.weight
        return search_result

    @staticmethod
    def _correct(from_states: tuple[Environment], to_states: tuple[Environment]) -> bool:
        return all(map(lambda tup: tup[0].correct(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _heuristic_mean(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return sum(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states))) / len(from_states)

    @staticmethod
    def _heuristic_min(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return min(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _heuristic_max(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return max(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _heuristic_sum(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return sum(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _find_program(node, reached):
        if node is None:
            return Program([])
        sequence = []
        while reached[node][1]:
            sequence.append(reached[node][2])
            node = reached[node][1]
        sequence.reverse()
        return Program(sequence)

    def save_node_stats(self, node, fcost, gcost, hcost):
        self.cost_per_iteration.append((self.number_of_iterations, hcost))
        self.g_cost_per_iteration.append((self.number_of_iterations, gcost))
        if hcost < self._best_cost:
            self._best_cost = hcost
            self._best_program_node = node
        if fcost < self._best_f_cost:
            self._best_f_cost = fcost
            self._best_f_program_node = node
        self.number_of_iterations += 1
        self.number_of_explored_programs += 1

    def best_first_search_upq(self, start_node: tuple[Environment], end_node: tuple[Environment],
                              tokens: list[Token], f, h) -> Iterator[Program]:
        self.reached = {start_node: (0, False, False)}  # for each reached node: (path_cost, previous_node, token_used)
        queue = UniquePriorityQueue()
        gcost = 0
        hcost = h(start_node, end_node)
        fcost = f(gcost, hcost)
        queue.insert(start_node, fcost)
        while queue:
            node, fcost = queue.pop()
            gcost, _, _ = self.reached[node]
            hcost = h(node, end_node)
            self.save_node_stats(node, fcost, gcost, hcost)
            if self._correct(node, end_node):
                self.best_program_node = node
                yield node
            else:
                yield None
            node_copies = [copy.deepcopy(node) for _ in tokens]
            for token, node_copy in zip(tokens, node_copies):
                try:
                    child = tuple(map(token.apply, node_copy))
                    gcost_child = gcost + token.number_of_tokens()
                    # if child was not yet expanded or our new gcost is the smallest up until now
                    if child not in self.reached or gcost_child < self.reached[child][0]:
                        self.reached[child] = gcost_child, node, token
                        hcost_child = h(child, end_node)
                        fcost_child = f(gcost_child, hcost_child)
                        queue.insert(child, fcost_child)
                except(InvalidTransition, LoopIterationLimitReached):
                    pass
        return
