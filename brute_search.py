import copy
from interpreter.interpreter import *
from pixel_environment.pixel_tokens import *


def print_p(p):
    print(p.sequence)

def print_ps(ps):
    l = []
    for p in ps:
        l.append(p.sequence)
    print(l)

# check
def loss(output_pairs):
    cum_loss = 0.0
    for output_pair in output_pairs:
        cum_loss = cum_loss + output_pair[0].distance(output_pair[1])
    return cum_loss

# check
def problem_solved(output_pairs):
    solved = True
    for output_pair in output_pairs:
        solved = solved and output_pair[0].equivalent(output_pair[1])
    return solved

# check
def extend_program(best_program, programs):
    updated_programs = programs.copy()
    for program in programs:
        potentially_better_program = Program(best_program.sequence + program.sequence)
        updated_programs.append(potentially_better_program)
    return updated_programs

# check
def find_best_program(programs, sample_inputs, sample_outputs):
    ordered_programs = []
    for program in programs:
        program_outputs = []
        try:
            for input in sample_inputs:
                used_input = copy.deepcopy(input)
                program_output = program.interp(used_input)
                program_outputs.append(program_output)
               # program_output = program.interp(used_input)

            output_pairs = list(zip(program_outputs, sample_outputs))
            cum_loss = loss(output_pairs)
            solved = problem_solved(output_pairs)
            if(solved):
                return program, cum_loss, solved
            ordered_programs.append((program, cum_loss, solved))
        except InvalidTransition:
            # program.interp(used_input)
            ordered_programs.append((program, float("inf"), False))
    ordered_programs = sorted(ordered_programs, key=lambda x: x[1])
    best_program, best_loss, solved = ordered_programs[0]
    return best_program, best_loss, solved

def synth_loop(programs, sample_inputs, sample_outputs, iteration, num_iterations):
    best_program, best_loss, solved = find_best_program(programs, sample_inputs, sample_outputs)
    print("The best loss currently is {}".format(best_loss))
    if(iteration >= num_iterations or solved):
        return best_program, best_loss, solved

    updated_programs = extend_program(best_program, programs)

    iteration = iteration + 1
    return synth_loop(updated_programs, sample_inputs, sample_outputs, iteration, num_iterations)

def search(tokens, examples, num_iterations):
    sample_inputs = list(map(lambda x: x.input_environment, examples))

    sample_outputs = list(map(lambda x: x.output_environment, examples))

    initial_programs = list(map(lambda x: Program([x]), tokens))
    iteration = 0
    best_program, best_loss, solved = synth_loop(initial_programs, sample_inputs, sample_outputs, iteration, num_iterations)

    return best_program, best_loss, solved

