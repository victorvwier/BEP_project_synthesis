# VANILLA GENETIC PROGRAMMING ALGORITHM

import math
import sys
import random, itertools
from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import InvalidTransition, Token
from common.tokens.control_tokens import LoopIterationLimitReached
from search.abstract_search import SearchAlgorithm
from search.invent import invent2

from typing import List, Tuple
from math import inf
from heapq import *

# Draw from a list of options randomly (no seed)
def draw_from(options, number_of_elems=1, weights=None):
    return random.choices(options, weights=weights, k=number_of_elems)

def normalize_errors(errors):
	# Assumption: no negative errors
	inf_values, fin_values = [], []
	for err, _, _ in errors:
		if (math.isinf(err)):
			inf_values.append(err)
			continue
		fin_values.append(err)

	print(len(inf_values), len(fin_values))

	# If all values are infinite, then pick some max_err (here, 0.5)
	if(len(fin_values) == 0):
		max_err = 0.5
	else:
		max_err = max(fin_values)
		if (math.isclose(max_err, 0, rel_tol=1e-05, abs_tol=1e-08)):
			max_err = sys.float_info.max / (10 * len(inf_values)) # in order to maintain computable values (small)	

	norm_errors = []
	sum = 0.0
	for err, _, _ in errors:
		if(math.isinf(err)):
			inf_sub = max_err*2
			norm_errors.append(inf_sub)
			sum += inf_sub
			continue
		norm_errors.append(err)
		sum += err

	error_prob = [n_err/sum for n_err in norm_errors]
	sorted(error_prob, reverse=True)
	return error_prob

def chose_with_prob(prob):
	return draw_from([True, False], weights=[prob, 1.0-prob])[0]

def pairs_from(items):
	n = 2
	args = [iter(items)] * n
	return itertools.zip_longest(*args)

class VanillaGP(SearchAlgorithm):
	# Static fields
	examples = [] # training examples
	MAX_TOKEN_FUNCTION_DEPTH = 5 # used in the invention of tokens
	token_functions = []
	MAX_NUMBER_OF_GENERATIONS = 200
	mutation_chance = 35 # Chance of an individual gene(function) being mutated (may be changed to be random for each mutation(?))

	# Dynamic fields
	current_gen_num = 0
	# current_gen = []
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
		
	# --Selection Process--
	def program_fitness(self, program):
		try:
			cum_loss = 0.0
			solved = True
			for example in self.examples:
				input = example.input_environment
				output = example.output_environment
				program_output = program.interp(input)
				cum_loss += program_output.distance(output)
				solved = solved and program_output.correct(output)
			if (solved):
				return (cum_loss, 0, program)
			return (cum_loss, 1, program)
		except (InvalidTransition, LoopIterationLimitReached) as e:
			return (float("inf"), 1, program)

	def gen_fitness(self, gen):
		gen_fitness = []
		for program in gen:
			program_data = self.program_fitness(program)
			gen_fitness.append(program_data)
		gen_fitness = sorted(gen_fitness)
		return gen_fitness

	# -- Crossover --
	def pick_crossover_point(self, program):
		indices = range(0, len(program.sequence))
		chosen_index = draw_from(indices)[0]
		return chosen_index

	def one_point_crossover(self, program_x, program_y):
		seq_x = program_x.sequence
		seq_y = program_y.sequence
		crossover_point_x = self.pick_crossover_point(program_x)
		crossover_point_y = self.pick_crossover_point(program_y)
		# print(crossover_point_x)
		# print(crossover_point_y)
		updated_seq_x = seq_x[:crossover_point_x + 1] + seq_y[crossover_point_y + 1:]
		updated_seq_y = seq_y[:crossover_point_y + 1] + seq_x[crossover_point_x + 1:]

		child_x = Program(updated_seq_x)
		child_y = Program(updated_seq_y)

		return child_x, child_y

	def n_point_crossover(self, n, program_x, program_y, x_points, y_points):
		# Assumptions:
		# - points are sorted increasingly
		# - points are within range
		# - size of both point arrays is n
		# - points are unique

		seq_x = program_x.sequence
		seq_y = program_y.sequence

		cuts_x = []
		cuts_y = []

		start = 0
		for i in x_points:
			slice_i = seq_x[start:i+1]
			cuts_x.append(slice_i)
			start = i
		slice_tail = seq_x[start:]
		cuts_x.append(slice_tail)

		start = 0
		for i in y_points:
			slice_i = seq_y[start:i+1]
			cuts_y.append(slice_i)
			start = i
		slice_tail = seq_y[start:]
		cuts_y.append(slice_tail)

		for i in range(1, n+1):
			inter = cuts_x[i]
			cuts_x[i] = cuts_y[i]
			cuts_y[i] = inter

		child_x_seq = itertools.chain.from_iterable(cuts_x)
		child_y_seq = itertools.chain.from_iterable(cuts_y)

		child_x = Program(child_x_seq)
		child_y = Program(child_y_seq)

		return child_x, child_y

	# -- Mutation --
	def mutate_program(self, program):
		program_seq = program.sequence
		mutated_seq = []
		for function in program_seq:
			if(draw_from([True, False])):
				new_random_function = draw_from(self.token_functions)
				mutated_seq.append(new_random_function)
			else:
				mutated_seq.append(function)

		mutated_program = Program(program_seq)

		return mutated_program

	def mutate_gen(self, gen):
		mutated_gen = [self.mutate_program(program) for program in gen]
		return mutated_gen

	# -- Intermediate Generation --
	def intermediate_gen(self):
		intermediate_gen = []
		crossover_subset = []

		probs = normalize_errors(self.current_gen_fitness)
		for i in range(len(self.current_gen_fitness)):
			_, _, program = self.current_gen_fitness[i]
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

	def breed_generation(self):
		new_gen = self.intermediate_gen()
		new_gen = self.mutate_gen(new_gen)
		self.current_gen_num += 1
		return new_gen

	# General Interface

	def __init__(self, time_limit_sec: float):
		super().__init__(time_limit_sec)

	def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
		self.token_functions =  [token for token in list(trans_tokens)] + invent2(trans_tokens, bool_tokens, self.MAX_TOKEN_FUNCTION_DEPTH)
		self.examples = training_examples

		# Set the overall best results to the performance of the initial (empty) best program Program([])
		self._best_fitness, self._best_solved, self._best_program = self.program_fitness(self._best_program)

		# Parameters for the initial random population
		self.initial_population_size = 200
		self.max_prog_length = 20

		# Set the seed
		# random.seed(self.seed)

		# The current generation is the initial random generation at the beginning
		initial_gen = self.generate_rand_population(self.initial_population_size, self.max_prog_length)
		self.current_gen_fitness = self.gen_fitness(initial_gen)
		self.current_gen_num = 0
		self.number_of_iterations = 0
		self.number_of_explored_programs = self.initial_population_size

		self.cost_per_iteration = []

	def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
		current_best_fitness, current_best_solved, current_best_program = self.current_gen_fitness[0]
		self.cost_per_iteration.append((self.current_gen_num, current_best_fitness))

		print("----Gen", self.current_gen_num)
		print(current_best_fitness, current_best_solved, current_best_program)

		# fitness is actually the loss, hence the less-than sign. A bit unfortunate, but oh well
		if (current_best_solved == 0 or current_best_fitness < self._best_fitness):
			self._best_fitness = current_best_fitness
			self._best_solved = current_best_solved
			self._best_program = current_best_program

		if (self._best_solved == 0 or self.current_gen_num >= self.MAX_NUMBER_OF_GENERATIONS):
			return False

		next_gen = self.breed_generation()
		self.current_gen_fitness = self.gen_fitness(next_gen)

		self.number_of_iterations += 1
		self.number_of_explored_programs += len(self.current_gen_fitness)

		return True
