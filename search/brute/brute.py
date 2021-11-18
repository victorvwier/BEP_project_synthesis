import copy
from typing import Tuple
from common_environment.control_tokens import LoopIterationLimitReached, RecursiveCallLimitReached
from interpreter.interpreter import *
from parser.experiment import Example, TestCase
from pixel_environment.pixel_tokens import *
import heapq

from search.abstract_search import SearchAlgorithm
from search.invent import invent2

MAX_NUMBER_OF_ITERATIONS = 20
MAX_TOKEN_FUNCTION_DEPTH = 3

class Brute(SearchAlgorithm):
    
    def search(test_case: TestCase, trans_tokens, bool_tokens) -> Tuple[Program, int, int]:
        # generate different token combinations
        token_functions = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)
        # find program that satisfies training_examples
        program: Program
        return _search(token_functions, test_case.training_examples, MAX_NUMBER_OF_ITERATIONS)


# takes 90 % of our time
def evaluate_program(program, examples):
    try:
        cum_loss = 0.0
        solved = True
        for example in examples:
            input = example.input_environment
            output = example.output_environment
            program_output = program.interp(input)
            cum_loss += program_output.distance(output)
            solved = solved and program_output.correct(output)
        if (solved):
            return (cum_loss, 0, program)
        return ( cum_loss, 1, program)
    except (InvalidTransition, RecursiveCallLimitReached, LoopIterationLimitReached) as e:
        return (float("inf"), 1, program)

def extend_program(best_program, programs, tokens: List[Token], examples):
    for token in tokens:
        potentially_better_program = Program(best_program.sequence + [copy.copy(token)])
        program_new = evaluate_program(potentially_better_program, examples)
        if program_new[0] != float('inf'):
            heapq.heappush(programs, program_new)
    return programs


def synth_loop(programs, tokens: List[Token], examples, iteration, num_iterations):
    (best_loss, solved, best_program) = heapq.heappop(programs)

    if(iteration >= num_iterations or solved == 0):
        return best_loss, solved, best_program

    updated_programs = extend_program(best_program, programs, tokens, examples)

    iteration += 1
    return synth_loop(updated_programs, tokens, examples, iteration, num_iterations)

def _search(tokens: List[Token], examples: List[Example], num_iterations):
    #domain_tokens = [Program([t]) for t in tokens]
    
    #program_dictionary = copy.deepcopy(initial_programs)
    program = Program([])
    #programs = prioritize_programs(initial_programs, sample_inputs, sample_outputs)
    
    starting_heap = [(float('inf'), 1, program)]
    heapq.heapify(starting_heap)
    best_loss, solved, best_program = synth_loop(starting_heap, tokens, examples, 0, num_iterations)

    return best_program, best_loss, solved
