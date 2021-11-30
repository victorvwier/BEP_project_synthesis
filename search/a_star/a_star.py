import itertools
from heapq import *
from typing import Callable, Generator, Iterator

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


class AStar(SearchAlgorithm):
    _best_program: Program
    input_envs: tuple[Environment]
    output_envs: tuple[Environment]
    tokens: list[Token]
    loss_function: Callable[[int, int], int]
    program_generator: Iterator[Program]

    def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
        self.input_envs = tuple(e.input_environment for e in training_examples)
        self.output_envs = tuple(e.output_environment for e in training_examples)
        self.tokens = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)
        self.loss_function = lambda g, h: h
        self.program_generator = self.best_first_search(self.input_envs, self.output_envs, self.tokens, self.loss_function)

    def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
        self._best_program = next(self.program_generator)
        program_empty = not self._best_program.sequence
        return program_empty

    @staticmethod
    def _correct(from_states: tuple[Environment], to_states: tuple[Environment]) -> bool:
        return all(map(lambda tup: tup[0].correct(tup[1]), zip(from_states, to_states)))

    @staticmethod
    def _heuristic(from_states: tuple[Environment], to_states: tuple[Environment]) -> float:
        return sum(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states)))/len(from_states)

    def best_first_search(self, start_node: tuple[Environment], end_node: tuple[Environment], tokens: list[Token], f) -> Iterator[Program]:
        reached = {start_node: (0, False, False)}  # for each reached node: (path_cost, previous_node, token_used)
        queue = []
        count = itertools.count()
        heappush(queue, (f(0, self._heuristic(start_node, end_node)), next(count), start_node))
        node = False
        while queue:
            total_cost, _, node = heappop(queue)  # total_cost: the estimated cost for the total path
            path_cost, _, _ = reached[node]  # path_cost: the minimal cost so far for a path to this node
            if self._correct(node, end_node):
                break
            else:
                yield Program([])
            node_copies = [copy.deepcopy(node) for _ in tokens]
            for token, node_copy in zip(tokens, node_copies):
                try:
                    child = tuple(map(token.apply, node_copy))
                    if child not in reached or path_cost + token.number_of_tokens(1) < reached[child][0]:
                        reached[child] = path_cost + token.number_of_tokens(1), node, token
                        heappush(queue, (f(path_cost + token.number_of_tokens(1), self._heuristic(child, end_node)), next(count), child))
                        print(token)
                        print(child[0])
                # except(InvalidTransition, RecursiveCallLimitReached, LoopIterationLimitReached) as e:
                except:
                    pass
        # success = correct(node, end_node)
        sequence = []
        while reached[node][1]:
            sequence.append(reached[node][2])
            node = reached[node][1]
        sequence.reverse()
        yield Program(sequence)
