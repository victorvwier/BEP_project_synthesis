# VANILLA GENETIC PROGRAMMING ALGORITHM

import random, itertools, heapq
from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import InvalidTransition, Token
from common.tokens.control_tokens import LoopIterationLimitReached
from search.abstract_search import SearchAlgorithm
from search.invent import invent2

from typing import List, Tuple
from math import inf, modf
from heapq import *

# Draw from a list of options randomly (no seed)
def draw_from(options, number_of_elems=1):
    return random.choices(options, k=number_of_elems)

class VanillaGP(SearchAlgorithm):
	# Static fields
	examples = [] # training examples
	MAX_TOKEN_FUNCTION_DEPTH = 5 # used in the invention of tokens
	token_functions = []
	MAX_NUMBER_OF_GENERATIONS = 50
	mutation_chance = 35 # Chance of an individual gene(function) being mutated (may be changed to be random for each mutation(?))

	# Dynamic fields
	current_gen_num = 0
	current_gen = []
	current_gen_fitness = []
	best_fitness = float("inf")
	best_solved = 1

	# Genetic Algorithm

	def generate_rand_program(self, max_prog_length):
		prog_length = random.randint(1, max_prog_length)
		program_seq = []
		# for i in range(prog_length):
		# 	function = draw_from(self.token_functions)
		# 	program_seq.append(function)
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

	def gen_fitness(self):
		gen_fitness = []
		for program in self.current_gen:
			program_data = self.program_fitness(program)
			heapq.heappush(gen_fitness, program_data)
		return gen_fitness

	# -- Crossover --
	def one_point_crossover(self, program_x, program_y):
		# Pick a crossover point (cut in half for now)
		seq_x = program_x.sequence
		seq_y = program_y.sequence
		len_x = len(seq_x)
		len_y = len(seq_y)
		crossover_point_x = int(modf(len_x/2.0)[1])
		crossover_point_y = int(modf(len_y/2.0)[1])
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

		return mutated_genotype

	def mutate_gen(self):
		for program in self.current_gen:
			self.mutate_program(program)

	def intermediate_gen(self):
		intermediate_gen = []
		i = 0
		while i < len(self.current_gen_fitness):
			_, _, program_x = self.current_gen_fitness[i]
			reproduction_decision = False # draw_from_bin_with_chance(50)
			if(reproduction_decision or i == len(self.current_gen_fitness) - 1):
				intermediate_gen.append(program_x)
			else:
				i = i + 1
				_, _, program_y = self.current_gen_fitness[i]
				child_x, child_y = self.one_point_crossover(program_x, program_y)
				intermediate_gen.append(child_x)
				intermediate_gen.append(child_y)
			i = i + 1
		self.current_gen = intermediate_gen

	def breed_generation(self):
		self.intermediate_gen()
		# self.mutate_gen()
		self.current_gen_num += 1

	# General Interface

	def __init__(self, time_limit_sec: float):
		super().__init__(time_limit_sec)

	def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
		self.token_functions = invent2(trans_tokens, bool_tokens, self.MAX_TOKEN_FUNCTION_DEPTH) + [token for token in list(trans_tokens)]
		self.examples = training_examples

		# Set the overall best results to the performance of the initial (empty) best program Program([])
		self.best_fitness, self.best_solved, self._best_program = self.program_fitness(self._best_program)

		# Parameters for the initial random population
		self.initial_population_size = 100
		self.max_prog_length = 10

		# Set the seed
		# random.seed(self.seed)

		# The current generation is the initial random generation at the beginning
		self.current_gen = self.generate_rand_population(self.initial_population_size, self.max_prog_length)
		self.current_gen_fitness = self.gen_fitness()
		self.current_gen_num = 0

		self.cost_per_iteration = []

	def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
		# print("----Gen ", self.current_gen_num, "----")
		# [print(f, s, p) for f, s, p in self.current_gen_fitness]
		current_best_fitness, current_best_solved, current_best_program = self.current_gen_fitness[0]
		self.cost_per_iteration.append((self.current_gen_num, current_best_fitness))
		# print(current_best_fitness, current_best_solved, current_best_program)

		# fitness is actually the loss, hence the less-than sign. A bit unfortunate, but oh well
		if (current_best_solved == 0 or current_best_fitness < self.best_fitness):
			self.best_fitness = current_best_fitness
			self.best_solved = current_best_solved
			self._best_program = current_best_program

		if (self.best_solved == 0 or self.current_gen_num >= self.MAX_NUMBER_OF_GENERATIONS):
			#print(self.current_gen_num)
			self.number_of_iterations = self.current_gen_num
			self.number_of_explored_programs = self.number_of_iterations * self.initial_population_size
			return False

		self.breed_generation()
		self.current_gen_fitness = self.gen_fitness()

		return True
