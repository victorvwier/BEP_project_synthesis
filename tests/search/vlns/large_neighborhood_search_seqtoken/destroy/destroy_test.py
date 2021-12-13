import unittest

from common.tokens.control_tokens import *
from common.tokens.string_tokens import *
from search.vlns.large_neighborhood_search_seqtoken.destroy.block_destroy import BlockDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.multi_method_destroy import MultiMethodDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.sequence_destroy import SequenceDestroy
from search.vlns.large_neighborhood_search_seqtoken.destroy.single_destroy import SingleDestroy


class MyTestCase(unittest.TestCase):
    def p(self):
        return Program([
            MoveLeft(), MoveLeft(), MoveLeft(),
            LoopWhile(
                AtStart(),
                [MoveLeft(), MoveLeft(), MoveLeft()]
            ),
            If(
                AtStart(),
                [MoveLeft(), MoveLeft(), MoveLeft()],
                [MoveLeft(), MoveLeft(), MoveLeft()]
            ),
            MoveLeft(), MoveLeft(),
        ])

    def test_block_destroy(self):
        r = BlockDestroy(p_destroy=0.5).destroy(self.p())

        print(r)

    def test_single_destroy(self):
        r = SingleDestroy(p_env=0.5, p_bool=0.5).destroy(self.p())

        print(r)

    def test_sequence_destroy(self):
        r = SequenceDestroy(p_destroy=1, max_seq_size=2).destroy(self.p())

        print(r)

    def test_multimethod_destroy(self):
        d = MultiMethodDestroy(
            methods=[
                SingleDestroy(p_env=0.15, p_bool=0.0),
                SequenceDestroy(p_destroy=0.5, max_seq_size=3),
                BlockDestroy(p_destroy=1)
            ],
            weights=[1, 1, 1],
        )

        r = d.destroy(self.p())

        print(r)


if __name__ == '__main__':
    unittest.main()
