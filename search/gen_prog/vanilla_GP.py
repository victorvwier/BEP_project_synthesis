# VANILLA GENETIC PROGRAMMING ALGORITHM

import math
import statistics
import random, itertools
from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import InvalidTransition, Token
from common.tokens.control_tokens import LoopIterationLimitReached
from search.abstract_search import SearchAlgorithm
from search.invent import invent2

from typing import List
from math import inf

# Draw from a list of options randomly (no seed)
def draw_from(options, number_of_elems=0, weights=None):
	if (number_of_elems == 0):
		res = random.choices(options, weights=weights, k=1)[0]
		return res
	return random.choices(options, weights=weights, k=number_of_elems)

def normalize_fitness(current_gen_fitness):
	# Assumption: no negative errors
	inf_values, fin_values = [], []
	for err, _ in current_gen_fitness:
		if (math.isinf(err)):
			inf_values.append(err)
			continue
		fin_values.append(err)

	shift = 0
	max_fin_value = 0.5
	if (len(fin_values) != 0):
		max_fin_value = max(fin_values)

	if (math.isclose(max_fin_value, 0, rel_tol=1e-05, abs_tol=1e-08)):
		shift = 1
		max_fin_value += shift

	norm_errors = []
	sum = 0.0
	for err, program in current_gen_fitness:
		if(math.isinf(err)):
			inf_sub = max_fin_value*len(current_gen_fitness)
			norm_errors.append((inf_sub, program))
			sum += inf_sub
		else:
			shifted_error = err + shift
			norm_errors.append((shifted_error, program))
			sum += shifted_error

	error_prob = [(n_err/sum, program) for n_err, program in norm_errors]
	sorted(error_prob, reverse=True)
	return error_prob

def chose_with_prob(prob):
	return draw_from([True, False], weights=[prob, 1.0-prob])

def pairs_from(items):
	n = 2
	args = [iter(items)] * n
	return itertools.zip_longest(*args)

def generation_stats(gen_fitness):
	prog_lengths = [p.number_of_tokens()  for _, p in gen_fitness]
	prog_tokens = [len(p.sequence) for _, p in gen_fitness]
	std_dev_lengths = statistics.stdev(prog_lengths)
	std_dev_token = statistics.stdev(prog_tokens)
	print(std_dev_lengths, std_dev_token)
	print(statistics.mean(prog_lengths), statistics.mean(prog_tokens))

def roulette_wheel(gen_probabilities):
	wheel = []

	cum_probability = 0
	for probability, program in gen_probabilities:
		wheel.append((cum_probability, cum_probability + probability, program))
		cum_probability += probability
	
	return wheel

def select_on_wheel(wheel, pointer):
	# print("Wheel: ", wheel)
	try:
		for cum_probability, probability, program in wheel:
			if (cum_probability <= pointer and cum_probability + probability >= pointer):
				return program
			# print("Program not on the wheel: ", program, " pointer: ", pointer)
	except Exception as e:
		print("Something went wrong: pointer not on the wheel")

def select_N_on_wheel(wheel, N, stepsize, pointer):
	selected = []
	selected.append(select_on_wheel(wheel, pointer))
	for i in range(0, N-1):
		pointer += stepsize
		pointer %= pointer
		selected.append(select_on_wheel(wheel, pointer))
	return selected

class VanillaGP(SearchAlgorithm):
	# Static fields
	type = "UN"
	MAX_NUMBER_OF_GENERATIONS = 200
	MAX_TOKEN_FUNCTION_DEPTH = 5 # used in the invention of tokens
	training_examples = [] # training examples
	token_functions = []
	mutation_chance = 2 # Chance of an individual gene(function) being mutated (may be changed to be random for each mutation(?))

	# Dynamic fields
	current_gen_num = 0
	current_gen_fitness = []

	_best_fitness = float("inf")
	_best_solved = 1

	# Genetic Algorithm

	def generate_rand_program(self, max_prog_length):
		prog_length = random.randint(1, max_prog_length)
		program_seq = []
		program_seq = draw_from(self.token_functions, number_of_elems=prog_length)
		return Program(program_seq)

	def generate_rand_population(self, population_size, max_prog_length):
		population = []
		for i in range(population_size):
			program = self.generate_rand_program(max_prog_length)
			population.append(program)
		return population
		
	# -- Fitness --
	def evaluate_program(self, program):
		try:
			cum_loss = 0.0
			solved = True
			for example in self.training_examples:
				input = example.input_environment
				output = example.output_environment
				program_output = program.interp(input)
				cum_loss += program_output.distance(output)
				solved = solved and program_output.correct(output)
			if (solved):
				error = 0
				return (error, program)
			else:
				error = cum_loss
				# print(solved)
				return (error, program)
		except (InvalidTransition, LoopIterationLimitReached) as e:
			error = float("inf")
			return (error, program)

	def gen_error(self):
		current_gen_error = []
		for program in self.current_gen:
			program_error = self.evaluate_program(program)
			current_gen_error.append(program_error)
		current_gen_error = sorted(current_gen_error)

		return current_gen_error

	def program_fitness(self, error):
		if (str(error) == "0" or math.isclose(error, 0, rel_tol=1e-05, abs_tol=1e-08)):
			return float("inf")
		elif (str(error) == "inf"):
			return 0
		else:
			return 1.0 / error

	def gen_fitness(self, current_gen_error):
		current_gen_fitness = []
		for error, program in current_gen_error:
			fitness = self.program_fitness(error)
			current_gen_fitness.append((fitness, program))

		# Sort [(error, program)] by error decreasingly
		current_gen_fitness = sorted(current_gen_fitness, reverse=True)

		return current_gen_fitness

	# -- Crossover --
	def pick_crossover_point(self, program):
		indices = range(0, len(program.sequence))
		chosen_index = draw_from(indices)
		return chosen_index

	def one_point_crossover(self, program_x, program_y):
		seq_x = program_x.sequence
		seq_y = program_y.sequence

		if (len(seq_x) == 0 or len(seq_y) == 0):
			return program_x, program_y

		crossover_point_x = self.pick_crossover_point(program_x)
		crossover_point_y = self.pick_crossover_point(program_y)

		# print(crossover_point_x)
		# print(crossover_point_y)

		updated_seq_x = seq_x[:crossover_point_x + 1] + seq_y[crossover_point_y + 1:]
		updated_seq_y = seq_y[:crossover_point_y + 1] + seq_x[crossover_point_x + 1:]

		child_x = Program(updated_seq_x)
		child_y = Program(updated_seq_y)

		return child_x, child_y

	def n_point_crossover(self, program_x, program_y):
		# Assumptions:
		# - points are sorted increasingly
		# - points are within range
		# - size of both point arrays is n
		# - points are unique

		seq_x = program_x.sequence
		seq_y = program_y.sequence

		# print(len(seq_x))
		# print(len(seq_y))

		min_length = min(len(seq_x), len(seq_y))
		if (min_length <= 1):
			return program_x, program_y

		n = random.randint(1, int(min_length/2))
		# print("n =", n)

		x_points = sorted(random.sample(range(0, len(seq_x)), n))
		y_points = sorted(random.sample(range(0, len(seq_y)), n))

		# print("x_points =", x_points)
		# print("y_points =", y_points)

		cuts_x = []
		cuts_y = []

		start = 0
		for i in x_points:
			slice_i = seq_x[start:i+1]
			cuts_x.append(slice_i)
			start = i+1
		slice_tail = seq_x[start:]
		cuts_x.append(slice_tail)

		start = 0
		for i in y_points:
			slice_i = seq_y[start:i+1]
			cuts_y.append(slice_i)
			start = i+1
		slice_tail = seq_y[start:]
		cuts_y.append(slice_tail)

		# print("cuts_x = ", cuts_x)
		# print("cuts_y = ", cuts_y)

		for i in range(0, n+1):
			if (i % 2 != 0):
				inter = cuts_x[i]
				cuts_x[i] = cuts_y[i]
				cuts_y[i] = inter

		child_x_seq = list(itertools.chain.from_iterable(cuts_x))
		child_y_seq = list(itertools.chain.from_iterable(cuts_y))

		# print(len(child_x_seq))
		# print(len(child_y_seq))

		child_x = Program(child_x_seq)
		child_y = Program(child_y_seq)

		return child_x, child_y

	def gen_crossover(self, gen):
		children = []

		# Iterate over the programs by 2 to pair them up
		i = 0
		while i < len(gen):
			program_x, program_y = gen[i], gen[i+1]
			child_x, child_y = None, None
			if (self.type == "O" or self.type == "U"):
				child_x, child_y = self.one_point_crossover(program_x, program_y)
			else:
				child_x, child_y = self.n_point_crossover(program_x, program_y)
			children.append(child_x)
			children.append(child_y)
			i += 2

		return children

	# --Selection Process--
	def selection(self, current_gen_fitness):
		intermediate_gen = []
		crossover_subset = []

		probs = normalize_fitness(current_gen_fitness)
		for i in range(len(current_gen_fitness)):
			_, program = current_gen_fitness[i]
			prob = probs[i]
			chosen = chose_with_prob(prob)
			if(chosen):
				intermediate_gen.append(program)
				continue
			crossover_subset.append(program)

		# MAKE SURE THAT CROSSOVER SUBSET HAS EVEN NUMBER OF ELEMENTS
		if(len(crossover_subset) % 2 != 0):
			intermediate_gen.append(crossover_subset[0])
			crossover_subset = crossover_subset[1:]

		children = []
		random.shuffle(crossover_subset)
		for program_x, program_y in pairs_from(crossover_subset):
			child_x, child_y = self.one_point_crossover(program_x, program_y)
			children.append(child_x)
			children.append(child_y)

		intermediate_gen = intermediate_gen + children

		return intermediate_gen
	
	def SUS(self, N, gen_probabilities):
		stepsize = 1.0 / N
		pointer = random.uniform(0, 1)

		wheel = roulette_wheel(gen_probabilities)

		selected_programs = select_N_on_wheel(wheel, N, stepsize, pointer)

		return selected_programs

	def selection_SUS(self, current_gen_fitness):
		N = len(current_gen_fitness)
		gen_probabilities = normalize_fitness(current_gen_fitness)

		intermediate_gen = []
		intermediate_gen = self.SUS(N, gen_probabilities)
		random.shuffle(intermediate_gen) # for extra stochasticity

		children = self.gen_crossover(intermediate_gen)

		return children

	# -- Mutation --
	def classical_mutation(self, program):
		program_seq = program.sequence
		mutated_seq = []
		for function in program_seq:
			if(draw_from([True, False], weights=[self.mutation_chance, 100 - self.mutation_chance])):
				new_random_function = draw_from(self.token_functions)
				mutated_seq.append(new_random_function)
			else:
				mutated_seq.append(function)

		mutated_program = Program(mutated_seq)

		return mutated_program

	def UMAD(self, program):
		genome_initial = program.sequence
		genome_intermediate = []
		genome_final = []

		addRate = 0.09
		delRate = addRate / (addRate + 1)

		# Addition step
		for gene in genome_initial:
			if random.uniform(0, 1) < addRate:
				new_gene = draw_from(self.token_functions)
				if random.uniform(0, 1) < 0.5:
					genome_intermediate.append(new_gene)
					genome_intermediate.append(gene)
				else:
					genome_intermediate.append(gene)
					genome_intermediate.append(new_gene)
			else:
				genome_intermediate.append(gene)

		# Deletion step
		for gene in genome_intermediate:
			if random.uniform(0, 1) < delRate:
				continue
			else:
				genome_final.append(gene)

		new_program = Program(genome_final)
		return new_program

	def mutate_gen(self, gen):
		mutated_gen = []
		if (self.type == "O" or self.type == "N"):
			mutated_gen = [self.classical_mutation(program) for program in gen]
		else:
			mutated_gen = [self.UMAD(program) for program in gen]
		return mutated_gen

	# -- Breed Next Generation
	def breed_generation(self, current_gen_fitness):
		new_gen = self.selection_SUS(current_gen_fitness)
		new_gen = self.mutate_gen(new_gen)
		self.current_gen_num += 1
		return new_gen

	# General Interface

	def __init__(self, time_limit_sec: float):
		super().__init__(time_limit_sec)

	def extend_result(self, search_result):
		search_result.dictionary['initial_error'] = self.initial_error
		return super().extend_result(search_result)

	def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
		self.token_functions =  [token for token in list(trans_tokens)] + invent2(trans_tokens, bool_tokens, self.MAX_TOKEN_FUNCTION_DEPTH)
		self.training_examples = training_examples

		# Set the overall best results to the performance of the initial (empty) best program Program([])
		self._best_error, self._best_program = self.evaluate_program(self._best_program)

		# Record the initial error (error of the empty program) in the SearchResult
		self.initial_error = self._best_error

		# Parameters for the initial random population
		self.initial_population_size = 200
		self.max_prog_length = 10

		# print("Type =", self.type)
		# print("Max Number of Generations", self.MAX_NUMBER_OF_GENERATIONS)
		# print("Population size =", self.initial_population_size)
		# print("Max Program Length =", self.max_prog_length)

		# The current generation is the initial random generation at the beginning
		initial_gen = self.generate_rand_population(self.initial_population_size, self.max_prog_length)
		self.current_gen = initial_gen

		self.current_gen_num = 0
		self.number_of_iterations = 0
		self.number_of_explored_programs = self.initial_population_size
		self.cost_per_iteration = []

	def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
		# Collect statistics about generation

		# Calculate the error for each program in the current generation
		current_gen_error = self.gen_error()

		self.number_of_explored_programs += len(self.current_gen)

		# Get the program with the lowest error
		current_best_error, current_best_program = current_gen_error[0]
		self.cost_per_iteration.append((self.current_gen_num, current_best_error))

		if (str(current_best_error) == "0" or current_best_error < self._best_error):
			self._best_error = current_best_error
			self._best_program = current_best_program

		if (str(current_best_error) == "0" or self.current_gen_num >= self.MAX_NUMBER_OF_GENERATIONS):
			return False

		current_gen_fitness = self.gen_fitness(current_gen_error)

		# print("----Gen ", self.current_gen_num, "----")
		# generation_stats(current_gen_fitness)

		next_gen = self.breed_generation(current_gen_fitness)
		self.current_gen = next_gen

		self.number_of_iterations += 1

		return True
