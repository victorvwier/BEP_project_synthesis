from common.tokens.control_tokens import LoopIterationLimitReached
from common.prorgam import *
from common.tokens.pixel_tokens import *
import copy
import heapq

from search.abstract_search import SearchAlgorithm
from search.invent import invent2

MAX_NUMBER_OF_ITERATIONS = 10
MAX_TOKEN_FUNCTION_DEPTH = 3


class Brute(SearchAlgorithm):

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)
        self.token_functions = []
        self.sample_inputs: List[Environment] = []
        self.sample_outputs: List[Environment] = []
        self.programs = []

    def setup(self, examples, trans_tokens, bool_tokens):

        # generate different token combinations
        self.token_functions = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)

        self.sample_inputs = [e.input_environment for e in examples]
        self.sample_outputs = [e.output_environment for e in examples]
        self.programs = [(float('inf'), 1, self._best_program)]
        heapq.heapify(self.programs)

    def iteration(self, examples, trans_tokens, bool_tokens) -> bool:

        (_, solved, self._best_program) = heapq.heappop(self.programs)

        if solved == 0:
            # return False to indicate no more iterations are necessary
            return False

        self.programs = extend_program(
            self._best_program, self.programs, self.token_functions, self.sample_inputs, self.sample_outputs)

        # return True to indicate that another iteration is required
        return True

def print_p(p):
    print(p.sequence)


def print_ps(ps):
    l = []
    for p in ps:
        l.append(p.sequence)
    print(l)


def loss(output_pairs):
    return sum([p[0].distance(p[1]) for p in output_pairs])


def problem_solved(output_pairs):
    return all(map(lambda p: p[0].correct(p[1]), output_pairs))


# takes 90 % of our time
def evaluate_program(program, sample_inputs, sample_outputs):
    program_outputs = []
    try:
        for input in sample_inputs:
            program_output = program.interp(input)
            program_outputs.append(program_output)
        output_pairs = list(zip(program_outputs, sample_outputs))
        cum_loss = loss(output_pairs)
        solved = problem_solved(output_pairs)
        if (solved):
            return (cum_loss, 0, program)
        return (cum_loss, 1, program)
    except (InvalidTransition, LoopIterationLimitReached) as e:
        return (float("inf"), 1, program)


def extend_program(best_program, programs, tokens: list[Token], sample_inputs, sample_outputs):
    for token in tokens:
        potentially_better_program = Program(best_program.sequence + [copy.copy(token)])
        program_new = evaluate_program(potentially_better_program, sample_inputs, sample_outputs)
        if program_new[0] != float('inf'):
            heapq.heappush(programs, program_new)
    # updated_programs = sorted(updated_programs, key=lambda x: (x[2], x[1]))
    return programs

