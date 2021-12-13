import unittest

from common.tokens.control_tokens import *
from common.tokens.string_tokens import *
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SequenceToken


class MyTestCase(unittest.TestCase):
    def p(self):
        return Program([
            LoopWhile(
                AtStart(),
                [If(
                    AtEnd(),
                    [MoveRight()],
                    [MoveLeft()]
                ), MoveLeft()]
            ),
            If(
                AtStart(),
                [MoveLeft(), MoveLeft()],
                [MoveRight()]
            ),
        ])

    def test_from_list(self):
        r = SequenceToken.from_list(self.p().sequence)

        print(r)

    def test_to_list(self):
        r = SequenceToken.from_list(self.p().sequence).to_list()

        print(r)


if __name__ == '__main__':
    unittest.main()
