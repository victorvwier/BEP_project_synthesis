from vlns.large_neighborhood_search.cost import Cost
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.probabilistic_destroy_expanding_sequences import \
    ProbabilisticDestroyExpandingSequences
from vlns.large_neighborhood_search.large_neighborhood_search import LNS
from vlns.large_neighborhood_search.implementations.greedy_lns.probabilistic_repair import ProbabilisticProgramRepair


class GreedyLNS(LNS):

    def __init__(self, domain: str):
        super().__init__(
            domain=domain,
            accept=DeterministicAccept(),
            #destroy=ProbabilisticProgramDestroy(prob=0.4,),
            destroy=ProbabilisticDestroyExpandingSequences(prob=0.4),
            repair=ProbabilisticProgramRepair(
                domain=domain,
                p_remove=0.3,
                p_split=1
            ),
            cost=Cost(),
            max_iterations=1000,
            max_token_function_depth=3,
        )