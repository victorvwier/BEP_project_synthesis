from common.prorgam import Program
from search.vlns.large_neighborhood_search_seqtoken.accept.accept import Accept


class DeterministicAccept(Accept):
    """Implements the deterministic accept method. A solution is accepted if and only if the cost is lower."""

    def accept(self, cost_current: float, cost_temporary: float, program_current: Program, program_temporary: Program, iteration: int) -> bool:
        # If cost is equal, accept the one with less characters
        if cost_temporary == cost_current:
            return program_temporary.number_of_tokens() <= program_current.number_of_tokens()

        # Else only accept if the new cost is better than the old one.
        return cost_temporary <= cost_current
