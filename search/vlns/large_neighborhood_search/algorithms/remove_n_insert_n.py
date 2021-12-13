from itertools import chain

from search.vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search.destroy.remove_n_destroy import ExtractNDestroy
from search.vlns.large_neighborhood_search.destroy.remove_n_destroy_2 import ExtractNDestroy2
from search.vlns.large_neighborhood_search.invent.variable_depth_invent import VariableDepthInvent
from search.vlns.large_neighborhood_search.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search.repair.insert_n_repair import InsertNRepair
from search.vlns.large_neighborhood_search.repair.insert_n_repair2 import InsertNRepair2


class RemoveNInsertN(LNS):

    def __init__(self, time_limit=10):
        super().__init__(
            time_limit=time_limit,
            accept=StochasticAccept(initial_temperature=0.1, cooling_factor=0.9997),
            destroy=ExtractNDestroy2(initial_max_n=3, max_max_n=3),
            repair=InsertNRepair2(initial_max_n=3, max_max_n=3, w_trans=1, w_loop=1, w_if=0),
            max_invent_depth=2,
            max_invent_control_tokens=2,
            increase_depth_after=15000,
            debug=False,
        )
