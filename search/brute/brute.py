from common.tokens.control_tokens import LoopIterationLimitReached
from common.prorgam import *
from common.tokens.pixel_tokens import *
import copy
import heapq

from search.abstract_search import SearchAlgorithm
from search.brute.invent import invent2, Invent
from search.search_result import SearchResult

MAX_NUMBER_OF_ITERATIONS = 10
MAX_TOKEN_FUNCTION_DEPTH = 3


class Brute(SearchAlgorithm):

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)
        self.token_functions = []
        self.sample_inputs: list[Environment] = []
        self.sample_outputs: list[Environment] = []
        self.programs = []
        self._best_program = Program([])
        self.best_cost = float("inf")
        self.current_program: Program = Program([])


    def setup(self, examples, trans_tokens, bool_tokens):
        self.programs = []
        self._best_program = Program([])

        # generate different token combinations
        invent = Invent(trans_tokens, bool_tokens)
        invent.permutations(up_to_length=3)
        invent.ifs(max_branch_size=2)
        invent.loops(max_body_size=2)
        invent.loop_if(max_loop_body_size=2, max_branch_size=1)
        self.token_functions = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)

        self.sample_inputs = [e.input_environment for e in examples]
        self.sample_outputs = [e.output_environment for e in examples]
        self.programs = [(float('inf'), 1, self.current_program)]
        heapq.heapify(self.programs)

        self.number_of_explored_programs = 0
        self.cost_per_iteration = []   # save (iteration_number, cost) when new best_program is found
        self.program_length_per_iteration = []  # (iteration_number, program_length)
        self.number_of_iterations = 0

    def iteration(self, examples, trans_tokens, bool_tokens) -> bool:

        (cost, solved, self.current_program) = heapq.heappop(self.programs)

        self.cost_per_iteration.append((self.number_of_iterations, cost))
        self.program_length_per_iteration.append((self.number_of_iterations, self.current_program.number_of_tokens()))
        if cost < self.best_cost:
            self._best_program = self.current_program
            self.best_cost = cost

        if solved == 0:
            # return False to indicate no more iterations are necessary
            return False

        self.number_of_iterations += 1

        self.programs = self.extend_program(
            self.current_program, self.programs, self.token_functions, self.sample_inputs, self.sample_outputs)

        # return True to indicate that another iteration is required
        return True

    def extend_program(self, best_program, programs, tokens: list[Token], sample_inputs, sample_outputs):
        for token in tokens:
            potentially_better_program = Program(best_program.sequence + [copy.copy(token)])
            program_new = evaluate_program(potentially_better_program, sample_inputs, sample_outputs)
            self.number_of_explored_programs += 1
            if program_new[0] != float('inf'):
                heapq.heappush(programs, program_new)
        # updated_programs = sorted(updated_programs, key=lambda x: (x[2], x[1]))
        return programs

    def extend_result(self, search_result: SearchResult):
        search_result.dictionary['program_length_per_iteration'] = self.program_length_per_iteration
        return search_result


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



