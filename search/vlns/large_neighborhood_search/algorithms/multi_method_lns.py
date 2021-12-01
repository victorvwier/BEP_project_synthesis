from evaluation.experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name
from example_parser.string_parser import StringParser
from search.vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search.destroy.block_destroy import BlockDestroy
from search.vlns.large_neighborhood_search.destroy.multi_method_destroy import MultiMethodDestroy
from search.vlns.large_neighborhood_search.destroy.sequence_destroy import SequenceDestroy
from search.vlns.large_neighborhood_search.destroy.single_destroy import SingleDestroy
from search.vlns.large_neighborhood_search.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search.repair.multi_method_repair import MultiMethodRepair
from search.vlns.large_neighborhood_search.repair.random_repair import RandomRepair
from search.vlns.large_neighborhood_search.repair.stochastic_sequence_repair import StochasticSequenceRepair
from search.vlns.large_neighborhood_search.repair.stochastic_single_repair import StochasticSingleRepair


class MultiMethodLNS(LNS):

    def __init__(self):
        super().__init__(
            time_limit=1,
            accept=StochasticAccept(initial_temperature=100, cooling_factor=0.95),
            #accept=DeterministicAccept(),
            destroy=MultiMethodDestroy(
                methods=[
                    SingleDestroy(p_env=0.15, p_bool=0.0),
                    SequenceDestroy(p_destroy=0.5, max_seq_size=5),
                    BlockDestroy(p_destroy=0.5)
                ],
                weights=[1, 1, 1],
            ),
            repair=MultiMethodRepair(
                methods=[
                    RandomRepair(p_if=0.1, p_loop=0.2, p_remove=0, p_split=0.5),
                    StochasticSingleRepair(
                        p_if=0.1, p_loop=0.3, p_remove=0.1, p_split=0.3,
                        n_if=10, n_loop=10, n_bool=20, n_env=20),
                    StochasticSequenceRepair(
                        p_if=0.1, p_loop=0.2, p_remove=0, p_split=0,
                        n_seq=100, n_bool=20, max_sequence_size=10)
                ],
                weights=[1, 0, 3]
            ),
        )

if __name__ == "__main__":
    mmlns = MultiMethodLNS()

    tc = StringParser().parse_file("9-2-1.pl")
    envs = set([c() for c in extract_trans_tokens_from_domain_name("string")])
    bools = set([c() for c in extract_bool_tokens_from_domain_name("string")])

    r = mmlns.run(tc, envs, bools)
    p = r.dictionary["program"]
    c = mmlns.cost_train(tc, p)

    print("Final program: {}".format(p))
    print("Cost: {}".format(c))
    print("Execution time: {}".format(r.dictionary["execution_time"]))
    print(r.dictionary['best_cost_per_iteration'])
    print(r.dictionary['current_cost_per_iteration'])