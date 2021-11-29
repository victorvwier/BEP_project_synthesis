from vlns.large_neighborhood_search.accept import DeterministicAccept
from vlns.large_neighborhood_search.cost import Cost
from vlns.large_neighborhood_search.implementations.branch_shuffling.branch_extraction import BranchExtraction
from vlns.large_neighborhood_search.large_neighborhood_search import LNS
from vlns.large_neighborhood_search.implementations.branch_shuffling.branch_composition import BranchCompositionRepair


class BranchShuffling(LNS):

    def __init__(self, domain: str, max_iterations: int, max_token_function_depth: int):
        super().__init__(
            domain=domain,
            accept=DeterministicAccept(),
            #accept=StochasticAccept(10, 0.999),
            destroy=BranchExtraction(),
            repair=BranchCompositionRepair(
                domain=domain,
                p_add=1,
                p_remove=0.2,
                p_loop=0.05,
                p_if=0.05,
            ),
            #cost=CostWithProgramLength(
            #    f_inout=1000,
            #    f_length=0.001,
            #),
            cost=Cost(),
            max_iterations=max_iterations,
            max_token_function_depth=max_token_function_depth)