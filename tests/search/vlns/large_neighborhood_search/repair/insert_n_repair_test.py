import unittest
from collections import Sequence

from common.tokens.string_tokens import *
from evaluation.experiment_procedure import extract_trans_tokens_from_domain_name
from search.vlns.large_neighborhood_search.repair.insert_n_repair import InsertNRepair


class MyTestCase(unittest.TestCase):
    @staticmethod
    def seqs():
        return [[MoveLeft(), MoveRight()], [], [MakeLowercase()], [Drop()]]

    @staticmethod
    def tokens():
        return [c() for c in extract_trans_tokens_from_domain_name("string")]

    def test_n_is_0(self):
        p = self.seqs()

        r = InsertNRepair(token_library=self.tokens(), n_options=[0], n_weights=[1]).repair(p)

        self.assertEqual(4, len(r.sequence))
        print(r)

    def test_n_is_1(self):
        p = self.seqs()

        r = InsertNRepair(token_library=self.tokens(), n_options=[1], n_weights=[1]).repair(p)

        self.assertEqual(7, len(r.sequence))
        print(r)

    def test_n_is_2(self):
        p = self.seqs()

        r = InsertNRepair(token_library=self.tokens(), n_options=[2], n_weights=[1]).repair(p)

        self.assertEqual(10, len(r.sequence))
        print(r)


if __name__ == '__main__':
    unittest.main()
