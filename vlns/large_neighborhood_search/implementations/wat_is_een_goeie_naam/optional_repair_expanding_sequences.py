from vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from vlns.large_neighborhood_search.cost import Cost
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.optional_repair import OptionalRepair
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.probabilistic_destroy_expanding_sequences import \
    ProbabilisticDestroyExpandingSequences
from vlns.large_neighborhood_search.large_neighborhood_search import LNS


class OptionalRepairExpandingSequences(LNS):

    def __init__(self, domain: str, max_iterations: int,
                 max_token_function_depth: int):
        super().__init__(
            domain,
            DeterministicAccept(),
            ProbabilisticDestroyExpandingSequences(prob=0.05),
            OptionalRepair(domain=domain),
            Cost(),
            max_iterations,
            max_token_function_depth)
