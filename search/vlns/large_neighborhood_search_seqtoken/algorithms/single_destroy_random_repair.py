from search.vlns.large_neighborhood_search_seqtoken.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search_seqtoken.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search_seqtoken.destroy.single_destroy import SingleDestroy
from search.vlns.large_neighborhood_search_seqtoken.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search_seqtoken.repair.random_repair import RandomRepair
from search.vlns.parameter_tuning import ParameterTuning


class SingleDestroyRandomRepair(LNS):

    def __init__(self, par):
        super().__init__(
            time_limit=2,
            #accept=StochasticAccept(initial_temperature=1, cooling_factor=par),
            accept=DeterministicAccept(),
            destroy=SingleDestroy(prob=0.2),
            repair=RandomRepair(w_loop=1, w_if=1, w_remove=1, w_split=0, w_default=1),
            debug=False,
        )

if __name__ == "__main__":
    pt = ParameterTuning(
        domain="string",
        #files=([3],[56, 61, 71, 80, 87, 92, 96, 101, 102, 103, 114, 116, 121, 127, 137],range(1,6)),
        files=([3],range(51, 101),range(1, 2)),
        repetitions=5,
        search_cons=SingleDestroyRandomRepair,
        values=[0.01, 0.1, 0.5, 1, 2, 5],
        debug=False,
    )

    pt.run()