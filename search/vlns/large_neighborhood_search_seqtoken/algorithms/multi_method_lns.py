from evaluation.experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name, \
    StringEnvironment
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
from search.vlns.large_neighborhood_search_seqtoken.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search_seqtoken.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search_seqtoken.destroy.block_destroy import BlockDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.multi_method_destroy import MultiMethodDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.sequence_destroy import SequenceDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.single_destroy import SingleDestroy
from search.vlns.large_neighborhood_search_seqtoken.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search_seqtoken.repair.multi_method_repair import MultiMethodRepair
from search.vlns.large_neighborhood_search_seqtoken.repair.random_repair import RandomRepair
from search.vlns.large_neighborhood_search_seqtoken.repair.stochastic_sequence_repair import StochasticSequenceRepair
from search.vlns.large_neighborhood_search_seqtoken.repair.stochastic_single_repair import StochasticSingleRepair
from search.vlns.parameter_tuning import ParameterTuning


class MultiMethodLNS(LNS):

    def __init__(self, par):
        super().__init__(
            time_limit=1,
            accept=StochasticAccept(initial_temperature=100, cooling_factor=0.97),
            #accept=DeterministicAccept(),
            destroy=MultiMethodDestroy(
                methods=[
                    SingleDestroy(p_env=0.2, p_bool=0.3),
                    SequenceDestroy(p_destroy=0.5, max_seq_size=5),
                    BlockDestroy(p_destroy=0.5)
                ],
                weights=[1,1,1],
            ),
            repair=MultiMethodRepair(
                methods=[
                    RandomRepair(w_if=1, w_loop=1, w_remove=1, w_split=1, w_default=1),
                    StochasticSingleRepair(
                        p_if=0.2, p_loop=0.2, p_remove=0.2, p_split=0.2,
                        n_if=10, n_loop=10, n_bool=20, n_env=20),
                    StochasticSequenceRepair(
                        p_if=0.3, p_loop=0.3, p_remove=0, p_split=0,
                        n_seq=20, n_bool=20, max_sequence_size=10)
                ],
                weights=[1, 1, 1]
            ),
        )

if __name__ == "__main__":
    pt = ParameterTuning(
        domain="string",
        files=([1,2,3,4,5,6,7,8,9],range(102, 103),range(1,6)),
        repetitions=10,
        search_cons=MultiMethodLNS,
        values=[1],
    )

    pt.run()

if __name__ == "__main__0":
    mmlns = MultiMethodLNS(0)

    tc = StringParser().parse_file("9-103-1.pl")
    envs = set([c() for c in extract_trans_tokens_from_domain_name("string")])
    bools = set([c() for c in extract_bool_tokens_from_domain_name("string")])

    r= mmlns.run(tc.training_examples, envs, bools)
    p = r.dictionary["program"]
    c = mmlns.cost(tc.test_examples, p)

    print("Final program: {}".format(p))
    print("Cost: {}".format(c))
    print("Execution time: {}".format(r.dictionary["execution_time"]))
    #print(r.dictionary['best_cost_per_iteration'])
    #print(r.dictionary['current_cost_per_iteration'])