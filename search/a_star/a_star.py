import itertools
from heapq import *

from common.tokens.control_tokens import LoopIterationLimitReached, RecursiveCallLimitReached
from common.prorgam import *
from common.experiment import TestCase
from common.tokens.pixel_tokens import *

from search.abstract_search import SearchAlgorithm
from search.invent import invent2

# from common_environment.abstract_tokens import Token, BoolToken, TransToken
# from common_environment.control_tokens import LoopIterationLimitReached, RecursiveCallLimitReached
# from common_environment.environment import Environment
# from interpreter.interpreter import Program, InvalidTransition
# from search.abstract_search import SearchAlgorithm
# from parser.experiment import Example, TestCase
# from search.invent import invent2

MAX_NUMBER_OF_ITERATIONS = 20
MAX_TOKEN_FUNCTION_DEPTH = 3


class AStar(SearchAlgorithm):
    @staticmethod
    def search(test_case: TestCase, trans_tokens, bool_tokens) -> Program:
        # generate different token combinations
        token_functions = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)
        input_envs = [e.input_environment for e in test_case.training_examples]
        output_envs = [e.output_environment for e in test_case.training_examples]
        return AStar.a_star_search(input_envs, output_envs, token_functions)

    @staticmethod
    def a_star_search(input_envs: list[Environment], output_envs: list[Environment], tokens: list[Token]) -> Program:
        def a_star_loss(g, h):
            return h
            # return g + h
        result_program = best_first_search(tuple(input_envs), tuple(output_envs), tokens, a_star_loss)
        return result_program


def heuristic(from_states, to_states) -> float:
    return sum(map(lambda tup: tup[0].distance(tup[1]), zip(from_states, to_states)))/len(from_states)


def correct(from_states, to_states) -> bool:
    return all(map(lambda tup: tup[0].correct(tup[1]), zip(from_states, to_states)))


def best_first_search(start_node, end_node, tokens: list[Token], f):
    reached = {start_node: (0, False, False)}  # for each reached node: (path_cost, previous_node, token_used)
    queue = []
    count = itertools.count()
    heappush(queue, (f(0, heuristic(start_node, end_node)), next(count), start_node))
    node = False
    while queue:
        total_cost, _, node = heappop(queue)  # total_cost: the estimated cost for the total path
        path_cost, _, _ = reached[node]  # path_cost: the minimal cost so far for a path to this node
        if correct(node, end_node):
            break
        node_copies = [copy.deepcopy(node) for _ in tokens]
        for token, node_copy in zip(tokens, node_copies):
            try:
                child = tuple(map(token.apply, node_copy))
                if child not in reached or path_cost + token.number_of_tokens(1) < reached[child][0]:
                    reached[child] = path_cost + token.number_of_tokens(1), node, token
                    heappush(queue, (f(path_cost + token.number_of_tokens(1), heuristic(child, end_node)), next(count), child))
            except(InvalidTransition, RecursiveCallLimitReached, LoopIterationLimitReached) as e:
                pass
    # success = correct(node, end_node)
    sequence = []
    while reached[node][1]:
        sequence.append(reached[node][2])
        node = reached[node][1]
    sequence.reverse()
    return Program(sequence)
