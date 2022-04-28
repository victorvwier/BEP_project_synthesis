import random
from common.program import Program
from common.settings.settings import Settings
from solver.search.search_algorithm import SearchAlgorithm


class GeneticProgramming(SearchAlgorithm):
	"""Implements a search algorithm using genetic programming."""
	
	def __init__(self, population_size: int, p_mutation: float):
		"""Initializes a new instance given the settings, time limit (sec), debug mode, population size and mutation
		probability."""
		self.p_mutation = p_mutation
		self.population_size = population_size

		# Initialize generation and fitness array.
		self.generation = []
		self.fitness = []

	def setup(self):
		# Setup with initial random generation consisting of programs with size 1.
		self.generation = [Program(random.sample(self.tokens, k=1)) for _ in range(self.population_size)]
		self.fitness = [self._fitness(program) for program in self.generation]

	def iteration(self) -> bool:
		# Reproduce by randomly selecting two parents based on fitness.
		new_generation = []

		for _ in range(self.population_size):
			parents = random.choices(self.generation, weights=self.fitness, k=2)
			new_generation.extend(self._reproduce(parents[0], parents[1]))

		self.generation = new_generation

		# Calculate new fitness
		self.fitness = [self._fitness(program) for program in self.generation]

		# Repeat until zero-cost solution has been found.
		return self.best_cost != 0

	def _mutate(self, program: Program):
		# Mutate with a random given probability. Chooses one of three mutate methods.
		if random.random() < self.p_mutation:
			random.choices(
				[self._mutate_add, self._mutate_remove, self._mutate_replace],
				weights=[1, 0, 0],
				k=1
			)[0](program)

	def _reproduce(self, parent1: Program, parent2: Program):
		# Combines two programs to create two children

		# Determine cross over indices
		index1 = random.randint(0, len(parent1.sequence))
		index2 = random.randint(0, len(parent2.sequence))

		# Create children.
		child1 = Program(parent1.sequence[index1:] + parent2.sequence[:index2])
		child2 = Program(parent1.sequence[:index1] + parent2.sequence[index2:])

		# Mutate children (chance of actually mutating is determined in _mutate).
		self._mutate(child1)
		self._mutate(child2)

		return [child1, child2]

	def _fitness(self, program: Program):
		# Transform cost to fitness
		return 1 / (1 + self.evaluate(program)[0]) + 0.0001

	def _mutate_add(self, program: Program):
		# Appends a token to the given program
		program.sequence = program.sequence + [random.choice(self.tokens)]

	def _mutate_remove(self, program: Program):
		# Removes a token randomly from the given program.
		index = random.randint(0, len(program.sequence))

		program.sequence = program.sequence[:index] + program.sequence[:index + 1]

	def _mutate_replace(self, program: Program):
		# Replaces a token randomly from the given program.
		index = random.randint(0, len(program.sequence))

		program.sequence = program.sequence[:index] + [random.choice(self.tokens)] + program.sequence[:index + 1]