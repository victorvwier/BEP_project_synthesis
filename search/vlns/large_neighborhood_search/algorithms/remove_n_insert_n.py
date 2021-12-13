from itertools import chain

from search.vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search.batch_run import BatchRun
from search.vlns.large_neighborhood_search.destroy.remove_n_destroy import ExtractNDestroy
from search.vlns.large_neighborhood_search.destroy.remove_n_destroy_2 import ExtractNDestroy2
from search.vlns.large_neighborhood_search.invent.variable_depth_invent import VariableDepthInvent
from search.vlns.large_neighborhood_search.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search.repair.insert_n_repair import InsertNRepair
from search.vlns.large_neighborhood_search.repair.insert_n_repair2 import InsertNRepair2


class RemoveNInsertN(LNS):

    def __init__(self):
        super().__init__(
            time_limit=10,
            accept=StochasticAccept(initial_temperature=0.1, cooling_factor=0.9997),
            #accept=DeterministicAccept(),
            #destroy=ExtractNDestroy(p_extract=0.2, n_options=[0, 1, 2], n_weights=[1, 1, 1]),
            destroy=ExtractNDestroy2(initial_max_n=3, max_max_n=3),
            #repair=InsertNRepair(n_options=[0, 1],n_weights=[1, 1],w_trans=1, w_loop=1, w_if=0),
            repair=InsertNRepair2(initial_max_n=3, max_max_n=3, w_trans=1, w_loop=1, w_if=0),
            invent=lambda t, b: VariableDepthInvent(t, b, max_depth=2, max_control_tokens=2),
            increase_depth_after=lambda depth: 15000,
            debug=False,
        )

if __name__ == "__main__":
    br = BatchRun(
        # Solves all
        #domain="robot",
        #files=([2,4,6,8,10], range(0, 10), range(0, 11)),
        #domain="pixel",
        #files=([1,2,3,4,5], range(0, 10), range(1, 11)),
        domain="string",
        files=([9], chain(range(51, 278), range(279, 328)), range(3,4)),
        #files=([9], range(51, 151), range(3,4)),
        #files=([9], range(1, 51), range(3,4)),
        #files=([9], [58], [3]),
        search_algorithm=RemoveNInsertN(),
        debug=True
    ).run()

