import random
from math import exp

from common.prorgam import Program
from search.vlns.large_neighborhood_search_seqtoken.accept.accept import Accept


class StochasticAccept(Accept):
    """Implements the stochastic accept method. A solution is always accepted if the new cost is lower. If the new cost
    is higher, the solution will be accepted with a probability of exp{-(new_cost - old_cost) / T}. Where T is the
    temperature. The temperature is set with an initial value and is multiplied by a constant factor each iteration."""

    def __init__(self, initial_temperature: float, cooling_factor: float):
        """Initializes the stochastic accept method. The initial temperature and cooling factor must be given."""
        assert 0 < cooling_factor #< 1

        self.temperature = initial_temperature
        self.cooling_factor = cooling_factor

        # Set iteration to -1 to denote it has not run any iteration yet.
        self.iteration = -1

    def accept(self, cost_current: float, cost_temporary: float, program_current: Program, program_temporary: Program, iteration: int) -> bool:
        # Set iteration to first seen iteration value.
        if self.iteration == -1:
            self.iteration = iteration

        # Whenever a new iteration begins, set new temperature.
        if iteration > self.iteration:
            self.iteration = iteration
            self.temperature *= self.cooling_factor

        # When equal, select with lowest number of tokens
        if cost_temporary == cost_current:
            return program_temporary.number_of_tokens() <= program_current.number_of_tokens()

        # When temporary is better or equal, accept.
        if cost_temporary <= cost_current:
            return True

        # Probability of accepting otherwise.
        prob = exp(-(cost_temporary - cost_current) / self.temperature)

        # Return true with that probability.
        return random.random() < prob