import unittest
from statistics import mean

from common.experiment import Example
from common.prorgam import Program
from common.tokens.control_tokens import LoopWhile, If
from common.tokens.string_tokens import *
from evaluation.experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name
from example_parser.string_parser import StringParser
from search.vlns.large_neighborhood_search_seqtoken.destroy.single_destroy import SingleDestroy
from search.vlns.large_neighborhood_search_seqtoken.repair.random_repair import RandomRepair
from search.vlns.large_neighborhood_search_seqtoken.repair.stochastic_sequence_repair import StochasticSequenceRepair
from search.vlns.large_neighborhood_search_seqtoken.repair.stochastic_single_repair import StochasticSingleRepair
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken


class MyTestCase(unittest.TestCase):

    @staticmethod
    def env_tokens():
        return [c() for c in extract_trans_tokens_from_domain_name("string")]

    @staticmethod
    def bool_tokens():
        return [c() for c in extract_bool_tokens_from_domain_name("string")]

    @staticmethod
    def test_case():
        return StringParser().parse_file("9-1-1.pl")

    @staticmethod
    def cost(seq: SeqToken):
        def ex_cost(ex: Example):
            try:
                return seq.apply(ex.input_environment).distance(ex.output_environment)
            except:
                return float('inf')

        return mean([ex_cost(ex) for ex in MyTestCase.test_case().training_examples])

    def p(self):
        return Program([
            MoveLeft(), MoveRight(), MakeUppercase(),
            LoopWhile(
                AtStart(),
                [MoveLeft(), MoveRight(), MakeUppercase()]
            ),
            If(
                AtStart(),
                [MoveLeft(), MoveLeft(), MoveLeft()],
                [MoveLeft(), MoveLeft(), MoveLeft()]
            ),
            MoveLeft(), MoveRight(), MakeUppercase()
        ])

    def test_single_random_repair(self):
        d = SingleDestroy(p_env=0.5, p_bool=0.5).destroy(self.p())
        print(d)

        rm = RandomRepair(
            p_if=0,
            p_remove=1,
            p_split=0,
            p_loop=0,
        )
        rm.set_token_libraries(self.env_tokens(), self.bool_tokens())
        r = rm.repair(d)

        print(r)

    def test_stochastic_single_repair(self):
        p = Program([
            LoopWhile(IsSpace(), [
                Drop(),
                MoveRight()
            ]),
        ])

        d = SingleDestroy(p_env=0.5, p_bool=1).destroy(p)
        print(d)

        rm = StochasticSingleRepair(
            p_if=0, p_loop=0.25, p_remove=0.25, p_split=0,
            n_if=9, n_loop=9, n_bool=9, n_env=9
        )
        rm.set_token_libraries(self.env_tokens(), self.bool_tokens())
        rm.cost = MyTestCase.cost
        r = rm.repair(d)

        print(r)

    def test_insert_sequence(self):
        d = SingleDestroy(p_env=0, p_bool=0).destroy(self.p())
        s = [MakeUppercase(), MakeLowercase(), MakeLowercase()]

        StochasticSequenceRepair._insert_sequence(d, s, 0)

        print(d)

    def test_get_destroyed_sequence_size(self):
        d = SingleDestroy(p_env=1, p_bool=0).destroy(self.p())
        s = StochasticSequenceRepair._destroyed_sequence_size(d)

        print(s)

if __name__ == '__main__':
    unittest.main()
