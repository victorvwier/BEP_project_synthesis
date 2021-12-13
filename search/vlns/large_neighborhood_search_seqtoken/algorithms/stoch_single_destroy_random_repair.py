from search.vlns.large_neighborhood_search_seqtoken.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search_seqtoken.destroy.single_destroy import SingleDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.stochastic_single_destroy import SingleStochasticDestroy
from search.vlns.large_neighborhood_search_seqtoken.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search_seqtoken.repair.random_repair import RandomRepair
from search.vlns.parameter_tuning import ParameterTuning


class SingleStochasticDestroyRandomRepair(LNS):

    def __init__(self, par):
        super().__init__(
            time_limit=1,
            #accept=StochasticAccept(initial_temperature=1, cooling_factor=par),
            accept=DeterministicAccept(),
            destroy=SingleStochasticDestroy(f_destroy=par, temperature=1),
            repair=RandomRepair(w_loop=1, w_if=1, w_remove=1, w_split=0, w_default=0),
        )

if __name__ == "__main__":
    pt = ParameterTuning(
        domain="string",
        #files=([3],[56, 61, 71, 80, 87, 92, 96, 101, 102, 103, 114, 116, 121, 127, 137],range(1,6)),
        files=([5],range(51, 101),range(1,2)),
        repetitions=1,
        search_cons=SingleStochasticDestroyRandomRepair,
        values=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5],
    )

    pt.run()