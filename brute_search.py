import heapq as hp

# class Program:
#     sequence = []
#
#     def __init__(self, data):
#         self.sequence = data
#
#     def get_functions(self):
#         return self.sequence
#
#     def append_function(self, function):
#         self.sequence.append(function)
#
#     def append_program(self, program):
#         new_sequence = self.sequence.copy()
#         functions = program.get_functions()
#         new_sequence.extend(functions)
#         return Program(new_sequence)
#
#     def eval(self, input):
#         state = input
#         for func in self.sequence:
#             state = func.apply(input)
#         return state

#def distance_measure(a, b):
#    return abs(a - b)

# Get the cumulative loss given a list [(program_output, desired_output)] and the distance measure

def loss(output_pairs):
    cum_loss = 0.0
    for output_pair in output_pairs:
        cum_loss = cum_loss + output_pair[0].distance(output_pair[1])
    return cum_loss

def extend_program(best_program, programs):
    updated_programs = programs.copy()
    for program in programs:
        potentially_better_program = Program(best_program.sequence + program.sequence)
        updated_programs.append(potentially_better_program)
    return updated_programs

def find_best_program(programs, sample_inputs, sample_outputs):
    ordered_programs = []  # [(cum_loss, Program)]
    for program in programs:
        program_output = []
        for input in sample_inputs:
            program_output.append(program.interp(input))
        cum_loss = loss(zip(program_output, sample_outputs))
        hp.heappush(ordered_programs, (cum_loss, program))

    best_program = hp.heappop(ordered_programs)
    return best_program, ordered_programs

def synth_loop(programs, sample_inputs, sample_outputs, iteration, num_iterations):
    if(iteration >= num_iterations):
        best_program, _ = find_best_program(programs, sample_inputs, sample_outputs)
        return best_program

    best_program, ordered_programs = find_best_program(programs, sample_inputs, sample_outputs)
    updated_programs = extend_program(best_program, programs)

    iteration = iteration + 1
    return synth_loop(updated_programs, sample_inputs, sample_outputs, iteration, num_iterations)

#samples :: [(Env, Env)]
#tokens :: [Token]
#num_iterations :: Int
def synth(tokens, samples, num_iterations):
    sample_inputs = list(map(lambda x: x[0], samples))
    sample_outputs = list(map(lambda x: x[1], samples))


    initial_programs = list(map(lambda x: Program([x]), tokens))
    iteration = 0
    best_program = synth_loop(initial_programs, sample_inputs, sample_outputs, iteration, num_iterations)

    return best_program
