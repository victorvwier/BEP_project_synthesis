import copy
from collections import Callable

from common_environment.control_tokens import LoopIterationLimitReached, RecursiveCallLimitReached
from interpreter.interpreter import *
from invent import invent2
from parser.experiment import Example
from pixel_environment.pixel_tokens import *
import heapq


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
    return all(map(lambda p : p[0].correct(p[1]), output_pairs))

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
        return ( cum_loss, 1, program)
    except (InvalidTransition, RecursiveCallLimitReached, LoopIterationLimitReached) as e:
        return (float("inf"), 1, program)


def extend_program(best_program, programs, program_dictionary, sample_inputs, sample_outputs):

    for token in program_dictionary:
        potentially_better_program = Program(best_program.sequence + token.sequence)

        program_new = evaluate_program(potentially_better_program, sample_inputs, sample_outputs)
        if program_new[0] != float('inf'):
            heapq.heappush(programs, program_new)

    #updated_programs = sorted(updated_programs, key=lambda x: (x[2], x[1]))
    return programs

# def prioritize_programs(programs, sample_inputs, sample_outputs):
#     ordered_programs = []
#     for program in programs:
#         ordered_programs.append(evaluate_program(program, sample_inputs, sample_outputs))
#     ordered_programs = sorted(ordered_programs, key=lambda x: (x[2], x[1]))
#     return ordered_programs

# def find_best_program(programs, sample_inputs, sample_outputs):
#     return prioritize_programs(programs, sample_inputs, sample_outputs)[0]

def synth_loop(programs, program_dictionary, sample_inputs, sample_outputs, iteration, num_iterations):
    #(best_loss, solved, best_program) = heapq.heappop(programs)
    (best_loss, solved, best_program) = programs[0]

    if(iteration >= num_iterations or solved == 0):
        return best_loss, solved, best_program

    updated_programs = extend_program(best_program, programs, program_dictionary, sample_inputs, sample_outputs)

    iteration += 1
    return synth_loop(updated_programs, program_dictionary, sample_inputs, sample_outputs, iteration, num_iterations)

def search(tokens, examples: List[Example], num_iterations):

    sample_inputs = [e.input_environment for e in examples]
    sample_outputs = [e.output_environment for e in examples]
    initial_programs = [Program([t]) for t in tokens]
    
    program_dictionary = copy.deepcopy(initial_programs)
    program = Program([])
    #programs = prioritize_programs(initial_programs, sample_inputs, sample_outputs)
    
    starting_heap = [(float('inf'), 1, program)]
    heapq.heapify([starting_heap])
    best_loss, solved, best_program = synth_loop(starting_heap, program_dictionary, sample_inputs, sample_outputs, 0, num_iterations)

    return best_program, best_loss, solved

"""
class Brute(ProgramSearch):

    def __init__(self, max_iterations: int, max_token_function_depth: int, domain: str):
        super().__init__(domain)
        self.max_iterations: max_iterations

        env_tokens = extract_trans_tokens_from_domain_name(domain)
        bool_tokens = extract_bool_tokens_from_domain_name(domain)
        self.tokens = invent2(env_tokens, bool_tokens, max_token_function_depth)

    def find(self, initial_solution: Environment, cost: Callable[[Environment], float]) -> Environment:
        return search(self.tokens, )

"""