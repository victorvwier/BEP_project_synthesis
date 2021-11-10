import heapq as hp
from common_environment.environment import *

def loss(output_pairs):
    cum_loss = 0.0
    for output_pair in output_pairs:
        cum_loss = cum_loss + output_pair[0].distance(output_pair[1])
    return cum_loss

def problem_solved(output_pairs):
    solved = False
    for output_pair in output_pairs:
        solved = solved and output_pair[0].equivalent(output_pair[1])
    return solved

def extend_program(best_program, programs):
    updated_programs = programs.copy()
    for program in programs:
        potentially_better_program = Program(best_program.sequence + program.sequence)
        updated_programs.append(potentially_better_program)
    return updated_programs

def find_best_program(programs, sample_inputs, sample_outputs):
    ordered_programs = []  # [(cum_loss, Program)]
    for program in programs:
        program_outputs = []
        for input in sample_inputs:
            program_output = program.interp(input)
            program_outputs.append(program_output)
        output_pairs = zip(program_outputs, sample_outputs)
        cum_loss = loss(output_pairs)
        solved = problem_solved(output_pairs)
        if(solved):
            return program, cum_loss, solved
        hp.heappush(ordered_programs, (cum_loss, program, solved))

    best_program, best_loss, solved = hp.heappop(ordered_programs)
    return best_program, best_loss, solved, ordered_programs

def synth_loop(programs, sample_inputs, sample_outputs, iteration, num_iterations):
    if(iteration >= num_iterations):
        best_program, best_loss, solved, _ = find_best_program(programs, sample_inputs, sample_outputs)
        return best_program, best_loss, solved

    best_program, best_loss, solved, ordered_programs = find_best_program(programs, sample_inputs, sample_outputs)
    # If the best program is solved, stop and return
    if(solved):
        return best_program, best_loss, solved

    updated_programs = extend_program(best_program, programs)

    iteration = iteration + 1
    return synth_loop(updated_programs, sample_inputs, sample_outputs, iteration, num_iterations)

def search(tokens, samples, num_iterations):
    sample_inputs = list(map(lambda x: x[0], samples))
    sample_outputs = list(map(lambda x: x[1], samples))

    initial_programs = list(map(lambda x: Program([x]), tokens))
    iteration = 0
    best_program, best_loss, solved = synth_loop(initial_programs, sample_inputs, sample_outputs, iteration, num_iterations)

    return best_program, best_loss, solved


