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

def loss(output_pairs):
    cum_loss = 0.0
    for output_pair in output_pairs:
        cum_loss = cum_loss + output_pair[0].distance(output_pair[1])
    return cum_loss

def problem_solved(output_pairs):
    solved = True
    for output_pair in output_pairs:
        solved = solved and output_pair[0].correct(output_pair[1])
    return solved

def evaluate_program(program, sample_inputs, sample_outputs):
    program_outputs = []
    try:
        for input in sample_inputs:
            used_input = copy.deepcopy(input)
            program_output = program.interp(used_input)
            program_outputs.append(program_output)
        output_pairs = list(zip(program_outputs, sample_outputs))
        cum_loss = loss(output_pairs)
        solved = problem_solved(output_pairs)
        if (solved):
            return (program, cum_loss, 0)
        return (program, cum_loss, 1)
    except InvalidTransition:
        return (program, float("inf"), 1)

def extend_program(best_program, programs, program_dictionary, sample_inputs, sample_outputs):
    updated_programs = programs
    for program in program_dictionary:
        potentially_better_program = Program(best_program.sequence + program.sequence)
        updated_programs.append(evaluate_program(potentially_better_program, sample_inputs, sample_outputs))
    updated_programs = sorted(updated_programs, key=lambda x: (x[2], x[1]))
    return updated_programs

def prioritize_programs(programs, sample_inputs, sample_outputs):
    ordered_programs = []
    for program in programs:
        ordered_programs.append(evaluate_program(program, sample_inputs, sample_outputs))
    ordered_programs = sorted(ordered_programs, key=lambda x: (x[2], x[1]))
    return ordered_programs

def find_best_program(programs, sample_inputs, sample_outputs):
    return prioritize_programs(programs, sample_inputs, sample_outputs)[0]

def synth_loop(programs, program_dictionary, sample_inputs, sample_outputs, iteration, num_iterations):
    for (p,l,s) in programs:
        print_p(p)
    print("Best:")
    (best_program, best_loss, solved) = programs[0]
    print_p(best_program)
    print(best_loss, solved)
    print("------------------------------------")
    #print("The best loss currently is {}".format(best_loss))
    if(iteration >= num_iterations or solved == 0):
        return best_program, best_loss, solved

    updated_programs = extend_program(best_program, programs[1:], program_dictionary, sample_inputs, sample_outputs)

    iteration = iteration + 1
    return synth_loop(updated_programs, program_dictionary, sample_inputs, sample_outputs, iteration, num_iterations)

def search(tokens, examples, num_iterations):
    sample_inputs = list(map(lambda x: x[0], examples))

    sample_outputs = list(map(lambda x: x[1], examples))

    initial_programs = list(map(lambda x: Program([x]), tokens))
    program_dictionary = copy.deepcopy(initial_programs)
    programs = prioritize_programs(initial_programs, sample_inputs, sample_outputs)
    iteration = 0
    best_program, best_loss, solved = synth_loop(programs, program_dictionary, sample_inputs, sample_outputs, iteration, num_iterations)

    return best_program, best_loss, solved
