from search.vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search.destroy.single_destroy import SingleDestroy
from search.vlns.large_neighborhood_search.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search.repair.random_repair import RandomRepair
from search.vlns.parameter_tuning import ParameterTuning


class SingleDestroyRandomRepair(LNS):

    def __init__(self, par):
        super().__init__(
            time_limit=1,
            #accept=StochasticAccept(initial_temperature=100, cooling_factor=0.95),
            accept=DeterministicAccept(),
            destroy=SingleDestroy(p_env=0.15, p_bool=0.2),
            repair=RandomRepair(w_loop=1, w_if=1, w_remove=1, w_split=par, w_default=1),
            #repair=StochasticSingleRepair(p_if=0.1, p_loop=0.3, p_remove=0.1, p_split=0.3, n_if=10, n_loop=10, n_bool=20, n_env=20),
        )

if __name__ == "__main__":
    pt = ParameterTuning(
        domain="string",
        files=([9],[56, 61, 71, 80, 87, 92, 96, 101, 102, 103, 114, 116, 121, 127, 137],range(1,5)),
        repetitions=1,
        search_cons=SingleDestroyRandomRepair,
        values=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8],
    )

    pt.run()